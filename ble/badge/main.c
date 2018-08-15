/*
 * Copyright (c) 2018 Owen Kirby
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/types.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <misc/printk.h>
#include <misc/util.h>
#include <kernel.h>
#include <console.h>
#include <crc16.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>

/* For UICR/Rabies tag programming */
#include <nrf.h>
#include <system_nrf51.h>

/* Generate and update beacons */
static void dc26_beacon_reset(void);
static void dc26_start_awoo(uint8_t ttl, uint16_t origin);

#define DC26_MAGIC_NONE		0x00
#define DC26_MAGIC_RABIES	0x35
#define DC26_MAGIC_AWOO 	0xa0
#define DC26_MAGIC_EMOTE	0xb2
#define DC26_MAGIC_VACCINE	0xce
#define DC26_APPEARANCE		0x26dc
#define DC26_MFGID_DCFURS	0x71ff

struct dc26_scan_data {
	char name[32];
	uint16_t appearance;
	uint16_t mfgid;
	uint16_t serial;
	uint8_t magic;
	uint8_t length;
	uint8_t payload[16];
};

static uint16_t dc26_badge_serial = 0xffff;

static void dc26_cure_rabies(void)
{
	if (NRF_UICR->CUSTOMER[0] != 0) {
		NRF_NVMC->CONFIG = NVMC_CONFIG_WEN_Wen << NVMC_CONFIG_WEN_Pos;
		while (NRF_NVMC->READY == NVMC_READY_READY_Busy) {
			;
		}
		NRF_UICR->CUSTOMER[0] = 0;
		while (NRF_NVMC->READY == NVMC_READY_READY_Busy) {
			;
		}
		NRF_NVMC->CONFIG = NVMC_CONFIG_WEN_Ren << NVMC_CONFIG_WEN_Pos;
		while (NRF_NVMC->READY == NVMC_READY_READY_Busy) {
			;
		}

		/* Update the beacon */
		dc26_beacon_reset();
	}
}

static uint32_t dc26_is_rabid(void)
{
	return (NRF_UICR->CUSTOMER[0] != 0);
}

/* Update the idle beacon content. */
static void dc26_beacon_reset(void)
{
	const struct bt_le_adv_param adv_param = {
		.options = 0,
		.interval_min = BT_GAP_ADV_SLOW_INT_MIN,
		.interval_max = BT_GAP_ADV_SLOW_INT_MAX,
	};

	/* Standard normally operating beacons. */
	u8_t adv_data[] = {
		(DC26_MFGID_DCFURS >> 0) & 0xff, /* DCFurs Cheaty Vendor ID */
		(DC26_MFGID_DCFURS >> 8) & 0xff,
		DC26_MAGIC_NONE,				 /* No Magic */
		(dc26_badge_serial >> 0) & 0xff, /* Serial */
		(dc26_badge_serial >> 8) & 0xff,
	};
	struct bt_data adv[] = {
		BT_DATA_BYTES(BT_DATA_GAP_APPEARANCE, (DC26_APPEARANCE & 0x00ff) >> 0, (DC26_APPEARANCE & 0xff00) >> 8),
		BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR),
		BT_DATA_BYTES(BT_DATA_NAME_COMPLETE, 'D', 'E', 'F', 'C', 'O', 'N', 'F', 'u', 'r', 's'),
		BT_DATA(BT_DATA_MANUFACTURER_DATA, adv_data, sizeof(adv_data))
	};

	/* Handle special bytes */
	if (dc26_badge_serial != 0xffff) {
	 	adv_data[2] = dc26_is_rabid() ? DC26_MAGIC_RABIES : DC26_MAGIC_NONE;
	}
	
	bt_le_adv_stop();
	bt_le_adv_start(&adv_param, adv, ARRAY_SIZE(adv), NULL, 0);
}

/* Timer/Workqueue handlers for clearing special beacons. */
static void dc26_magic_work(struct k_work *work) { dc26_beacon_reset(); }
K_WORK_DEFINE(dc26_magic_worker, dc26_magic_work);
static void dc26_magic_expire(struct k_timer *timer_id) { k_work_submit(&dc26_magic_worker); }
K_TIMER_DEFINE(dc26_magic_timer, dc26_magic_expire, NULL);

/* Start generating an Awoo beacon */
static void dc26_start_awoo(uint8_t ttl, uint16_t origin)
{
	if (!ttl) {
		return;
	}

	const struct bt_le_adv_param awoo_param = {
		.options = 0,
		.interval_min = BT_GAP_ADV_FAST_INT_MIN_2,
		.interval_max = BT_GAP_ADV_FAST_INT_MAX_2,
	};

	/* Awoo beacons */
	u8_t awoo_data[] = {
		(DC26_MFGID_DCFURS >> 0) & 0xff,
		(DC26_MFGID_DCFURS >> 8) & 0xff,
		DC26_MAGIC_AWOO,		/* Magic */
		(dc26_badge_serial >> 0) & 0xff, /* Serial */
		(dc26_badge_serial >> 8) & 0xff,
		ttl - 1,				/* TTL */
		(origin >> 0) & 0xff,	/* Origin */
		(origin >> 8) & 0xff,
	};
	struct bt_data awoo[] = {
		BT_DATA_BYTES(BT_DATA_GAP_APPEARANCE, (DC26_APPEARANCE & 0x00ff) >> 0, (DC26_APPEARANCE & 0xff00) >> 8),
		BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR),
		BT_DATA_BYTES(BT_DATA_NAME_COMPLETE, 'D', 'E', 'F', 'C', 'O', 'N', 'F', 'u', 'r', 's'),
		BT_DATA(BT_DATA_MANUFACTURER_DATA, awoo_data, sizeof(awoo_data))
	};

	bt_le_adv_stop();
	bt_le_adv_start(&awoo_param, awoo, ARRAY_SIZE(awoo), NULL, 0);
	k_timer_start(&dc26_magic_timer, K_SECONDS(5), 0);
}

/* Start generating an emote beacon */
static void dc26_start_emote(const char *hexstr)
{
	const struct bt_le_adv_param emote_param = {
		.options = 0,
		.interval_min = BT_GAP_ADV_FAST_INT_MIN_2,
		.interval_max = BT_GAP_ADV_FAST_INT_MAX_2,
	};
	/* Emote beacons */
	u8_t emote_data[] = {
		(DC26_MFGID_DCFURS >> 0) & 0xff,
		(DC26_MFGID_DCFURS >> 8) & 0xff,
		DC26_MAGIC_EMOTE,		/* Magic */
		(dc26_badge_serial >> 0) & 0xff, /* Serial */
		(dc26_badge_serial >> 8) & 0xff,
		0, 0, 0, 0, 0, 0, 0, 0	/* Emote data */
	};
	u8_t len = 5;
	while (len < sizeof(emote_data)) {
		u8_t hi, lo;
		char c;
		
		c = *hexstr++;
		if ((c >= '0') && (c <= '9')) hi = c - '0';
		else if ((c >= 'A') && (c <= 'F')) hi = c - 'A' + 10;
		else if ((c >= 'a') && (c <= 'f')) hi = c - 'a' + 10;
		else break;

		c = *hexstr++;
		if ((c >= '0') && (c <= '9')) lo = c - '0';
		else if ((c >= 'A') && (c <= 'F')) lo = c - 'A' + 10;
		else if ((c >= 'a') && (c <= 'f')) lo = c - 'a' + 10;
		else break;

		emote_data[len++] = (hi << 4) | lo;
	} /* while */

	struct bt_data emote[] = {
		BT_DATA_BYTES(BT_DATA_GAP_APPEARANCE, (DC26_APPEARANCE & 0x00ff) >> 0, (DC26_APPEARANCE & 0xff00) >> 8),
		BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR),
		BT_DATA_BYTES(BT_DATA_NAME_COMPLETE, 'D', 'E', 'F', 'C', 'O', 'N', 'F', 'u', 'r', 's'),
		BT_DATA(BT_DATA_MANUFACTURER_DATA, emote_data, len)
	};

	bt_le_adv_stop();
	bt_le_adv_start(&emote_param, emote, ARRAY_SIZE(emote), NULL, 0);
	k_timer_start(&dc26_magic_timer, K_SECONDS(5), 0);
}

/* Average RSSI Tracking */
#define DC26_RSSI_INIT			-80
#define DC26_RSSI_HISTORY_LEN	512
static s32_t dc26_rssi_sum = DC26_RSSI_INIT * DC26_RSSI_HISTORY_LEN;

/* Return the average RSSI */
static s8_t dc26_rssi_average(void)
{
	return dc26_rssi_sum / DC26_RSSI_HISTORY_LEN;
}

/* Update the average RSSI */
static void dc26_rssi_insert(s8_t rssi)
{
	static unsigned int idx = 0;
	static s8_t history[DC26_RSSI_HISTORY_LEN] = {
		[0 ... (DC26_RSSI_HISTORY_LEN-1)] = DC26_RSSI_INIT
	};

	/* Update the RSSI history. */
	s8_t prev = history[idx];
	history[idx] = rssi;
	idx = (idx + 1) % DC26_RSSI_HISTORY_LEN;

	/* Update the sum */
	dc26_rssi_sum -= prev;
	dc26_rssi_sum += rssi;
}

/* Cooldown timer between emotes. */
static s64_t dc26_emote_cooldown = 60000;
static s64_t dc26_emote_short_cooldown = 0;		/* For beacons with very high RSSI */
static s64_t dc26_emote_medium_cooldown = 0;	/* For beacons with average RSSI */
static s64_t dc26_emote_long_cooldown = 0;		/* For beacons with very weak RSSI */
static s64_t dc26_awoo_cooldown = 0;			/* For beacons starting a howl */

static s64_t dc26_emote_jitter(unsigned int max)
{
	return (max/2) + sys_rand32_get() % (max/2);
}

static void dc26_emote_reset_cooldowns(void)
{
	s64_t now = k_uptime_get();
	dc26_emote_short_cooldown = now + dc26_emote_jitter(dc26_emote_cooldown);
	dc26_emote_medium_cooldown = now + dc26_emote_jitter(dc26_emote_cooldown << 1);
	dc26_emote_long_cooldown = now + dc26_emote_jitter(dc26_emote_cooldown << 2);
}

static unsigned int dc26_emote_test_cooldowns(s8_t rssi)
{
	s64_t now = k_uptime_get();
	if (((rssi + 10) < dc26_rssi_average()) && (dc26_emote_long_cooldown > now)) {
		/* Beacon is 10dB below the average RSSI, and the long cooldown has not elapsed. */
		return 0; /* Long cooldown has not elapsed */
	}
	if ((rssi < -75) && (dc26_emote_medium_cooldown > now)) {
		return 0; /* Medium cooldown has not elapsed */
	}
	if (dc26_emote_short_cooldown > now) {
		return 0; /* Short cooldown has not elapsed */
	}

	/* Reset the cooldowns */
	dc26_emote_reset_cooldowns();
	return 1;
}

#if 0
/* bloom filter of blacklisted addresses */
static uint8_t 	dc26_blacklist[1024 / 8];

static void dc26_blacklist_insert(const bt_addr_le_t *addr)
{
	uint16_t ansi = crc16_ansi(addr->a.val, sizeof(addr->a.val));
	uint16_t ccitt = crc16_ccitt(addr->a.val, sizeof(addr->a.val));
	dc26_blacklist[(ansi >> 3) % sizeof(dc26_blacklist)] |= (1 << (ansi & 0x7));
	dc26_blacklist[(ccitt >> 3) % sizeof(dc26_blacklist)] |= (1 << (ccitt & 0x7));
}

static void dc26_blacklist_check(const bt_addr_le_t *addr)
{
	uint16_t ansi = crc16_ansi(addr->a.val, sizeof(addr->a.val));
	uint16_t ccitt = crc16_ccitt(addr->a.val, sizeof(addr->a.val));
	return (dc26_blacklist[(ansi >> 3) % sizeof(dc26_blacklist)] & (1 << (ansi & 0x7)) && 
			dc26_blacklist[(ccitt >> 3) % sizeof(dc26_blacklist)] & (1 << (ccitt & 0x7)));
}
#endif

static bool dc26_scan_parse(struct bt_data *ad, void *user_data)
{
	struct dc26_scan_data *scan = (struct dc26_scan_data *)user_data;

	switch (ad->type) {
		case BT_DATA_GAP_APPEARANCE:
			if (ad->data_len != 2) {
				scan->appearance = 0xffff;
				return false;
			}
			scan->appearance = (ad->data[1] << 8) | ad->data[0];
			break;
		
		case BT_DATA_NAME_COMPLETE:
		case BT_DATA_NAME_SHORTENED:
			if (ad->data_len >= sizeof(scan->name)) {
				scan->appearance = 0xffff;
				return false;
			}
			memcpy(scan->name, ad->data, ad->data_len);
			scan->name[ad->data_len] = '\0';
			break;
		
		case BT_DATA_MANUFACTURER_DATA:
			if (ad->data_len < 3) {
				scan->appearance = 0xffff;
				return false;
			}
			scan->mfgid = (ad->data[1] << 8) | ad->data[0];
			scan->magic = ad->data[2];
			if (ad->data_len >= 5) {
				scan->serial = (ad->data[3] << 8) | ad->data[4];
			}
			if (ad->data_len > 5) {
				scan->length = ad->data_len - 5;
				if (scan->length >= sizeof(scan->payload)) {
					scan->length = sizeof(scan->payload);
				}
				memcpy(scan->payload, &ad->data[5], scan->length);
			}
			break;
	}
	return true;
}

static void scan_cb(const bt_addr_le_t *addr, s8_t rssi, u8_t adv_type,
		    struct net_buf_simple *buf)
{
	char src[BT_ADDR_LE_STR_LEN];
	struct dc26_scan_data data;

	/* Parse the BLE advertisemnet. */
	memset(&data, 0, sizeof(data));
	data.appearance = 0xffff;
	bt_data_parse(buf, dc26_scan_parse, &data);
	if (data.appearance != DC26_APPEARANCE) {
		/* Not a part of the game - ignore it. */
		return;
	}

	bt_addr_le_to_str(addr, src, sizeof(src));

	if ((data.magic == DC26_MAGIC_EMOTE) && dc26_emote_test_cooldowns(rssi)) {
		/* Emote selection... */
		if (data.length < 2) {
			printk("rx: mfgid=0x%02x emote=random\n", data.mfgid);
		}
		else {
			char emhex[sizeof(data.payload)*2 + 1] = {'\0'};
			for (int i = 0; (i < sizeof(data.payload)) && i < data.length; i++) {
				sprintf(&emhex[i*2], "%02x", data.payload[i]);
			}
			printk("rx: mfgid=0x%02x rssi=%d emote=%s\n", data.mfgid, rssi, emhex);
		}
	}
	
	if ((data.magic == DC26_MAGIC_AWOO) && (data.mfgid == DC26_MFGID_DCFURS) &&
	    (dc26_awoo_cooldown < k_uptime_get()) && (data.length >= 3)) {
		/* Awoo beacon */
		uint8_t ttl = data.payload[0];
		uint16_t origin = (data.payload[2] << 8) | data.payload[1];
		printk("rx: awoo origin=0x%04x\n", origin);

		/* Route the magic beacon another hop */
		dc26_awoo_cooldown = k_uptime_get() + K_SECONDS(300);
		dc26_start_awoo(ttl, origin);
	}

	/* TODO: Do we want any other conditions to cure. */
	if ((data.magic == DC26_MAGIC_VACCINE) && (data.length >= 4) && (strncmp(data.payload, "CURE", 4) == 0)) {
		dc26_cure_rabies();
	}
	
	/* Enable for debug and RSSI tuning. */
#if 0
	else {
		printk("rx: mfgid=0x%02x rssi=%d avg=%d magic=%02x\n", data.mfgid, rssi, dc26_rssi_average(), data.magic);
	}
#endif

	/* Update RSSI tracking statistics */
	dc26_rssi_insert(rssi);
}

static void
do_set(int argc, char **argv)
{
	int i;
	for (i = 0; i < argc; i++) {
		/* In case the value is optional. */
		char *name = argv[i];
		char *value = strchr(argv[i], '=');
		if (value) *value++ = '\0';

		if (strcmp(name, "cooldown") == 0) {
			dc26_emote_cooldown = strtoul(value, NULL, 0);
			dc26_emote_reset_cooldowns();
		}
		if (strcmp(name, "serial") == 0) {
			dc26_badge_serial = strtoul(value, NULL, 0);
			dc26_beacon_reset();
		}
		if (strcmp(name, "vaccine") == 0) {
			dc26_cure_rabies();
		}
	}
}

static void
do_tx(int argc, char **argv)
{
	int i;
	for (i = 0; i < argc; i++) {
		/* In case the value is optional. */
		char *name = argv[i];
		char *value = strchr(argv[i], '=');
		if (value) *value++ = '\0';

		if (strcmp(name, "awoo") == 0) {
			dc26_awoo_cooldown = k_uptime_get() + K_SECONDS(300);
			dc26_start_awoo(64, dc26_badge_serial);
		}
		if (strcmp(name, "emote") == 0) {
			dc26_start_emote(value);
		}
	}
}

static void
do_echo(int argc, char **argv)
{
	int i;
	printk("echo:");
	for (i = 0; i < argc; i++) {
		printk(" %s", argv[i]);
	}
	printk("\n");
}

void
main(void)
{
	struct bt_le_scan_param scan_param = {
		.type       = BT_HCI_LE_SCAN_PASSIVE,
		.filter_dup = BT_HCI_LE_SCAN_FILTER_DUP_DISABLE,
		.interval   = 0x0010,
		.window     = 0x0010,
	};
	int err;

	console_getline_init();
	printk("Starting DC26 Badge Comms\n");

	/* Initialize the Bluetooth Subsystem */
	err = bt_enable(NULL);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return;
	}

	/* Start advertising */
	dc26_beacon_reset();
	dc26_emote_reset_cooldowns();

	err = bt_le_scan_start(&scan_param, scan_cb);
	if (err) {
		printk("Starting scanning failed (err %d)\n", err);
		return;
	}

	/* Run the console to handle input from the host. */
	while (1) {
		char *s = console_getline();
		char *name;
		char *args[16];
		int i;

		/* Each line should conform to the sytax of:
		 *     action: name=value ...
		 */
		name = strtok(s, ":");
		if (!name) {
			continue;
		}
		for (i = 0; i < sizeof(args)/sizeof(args[0]); i++) {
			args[i] = strtok(NULL, " ");
			if (!args[i]) break;
		}
		/* Some functions that we might care to run. */
		if (strcmp(name, "echo") == 0) {
			do_echo(i, args);
		}
		else if (strcmp(name, "set") == 0) {
			do_set(i, args);
			dc26_beacon_reset();
		}
		else if (strcmp(name, "tx") == 0) {
			do_tx(i, args);
		}
	}
}
