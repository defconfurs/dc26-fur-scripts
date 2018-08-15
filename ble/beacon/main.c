/*
 * Copyright (c) 2018 Owen Kirby
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/types.h>
#include <stddef.h>
#include <misc/printk.h>
#include <misc/util.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>

#include <board.h>
#include <device.h>
#include <gpio.h>

/* 1000 msec = 1 sec */
#define LED_INTERVAL_TIME 	3000
#define LED_BLINK_TIME		150

#define DEVICE_NAME CONFIG_BT_DEVICE_NAME
#define DEVICE_NAME_LEN (sizeof(DEVICE_NAME) - 1)

#define DC26_MAGIC_RABIES	0x35
#define DC26_MAGIC_EMOTE	0xb2
#define DC26_MAGIC_VACCINE	0xce
#define DC26_APPEARANCE		0x26dc

#if 1
static u8_t mfg_data[] = {
	0xcf, 0x0d,			/* DCFurs Beacon Vendor ID */
	DC26_MAGIC_EMOTE,	/* Magic */
	0x00, 0x00,			/* Serial */
	'^', '.', '^' 		/* Emote Selection */
};
#else
static u8_t mfg_data[] = {
	0xcf, 0x0d,			/* DCFurs Beacon Vendor ID */
	DC26_MAGIC_VACCINE,	/* Magic */
	0x00, 0x00,			/* Serial */
	'C', 'U', 'R', 'E'
};
#endif

static const struct bt_data adv[] = {
	BT_DATA_BYTES(BT_DATA_GAP_APPEARANCE, (DC26_APPEARANCE & 0x00ff) >> 0, (DC26_APPEARANCE & 0xff00) >> 8),
	BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR),
	BT_DATA_BYTES(BT_DATA_NAME_COMPLETE, 'D', 'E', 'F', 'C', 'O', 'N', 'F', 'u', 'r', 's'),
	BT_DATA(BT_DATA_MANUFACTURER_DATA, mfg_data, sizeof(mfg_data))
};

static struct bt_le_adv_param adv_param = {
	.options = 0,
	.interval_min = BT_GAP_ADV_SLOW_INT_MIN,
	.interval_max = BT_GAP_ADV_SLOW_INT_MAX,
};

static void bt_ready(int err)
{
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return;
	}

	printk("Bluetooth initialized\n");

	/* Start advertising */
	err = bt_le_adv_start(&adv_param, adv, ARRAY_SIZE(adv), NULL, 0);
	if (err) {
		printk("Advertising failed to start (err %d)\n", err);
		return;
	}

	printk("Beacon started\n");
}

void main(void)
{
	int err;
	struct device *dev;

	printk("Starting DCFurs Beacon\n");

	dev = device_get_binding(LED0_GPIO_PORT);
	/* Set LED pin as output */
	gpio_pin_configure(dev, LED0_GPIO_PIN, GPIO_DIR_OUT);


	/* Initialize the Bluetooth Subsystem */
	err = bt_enable(bt_ready);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
	}

	/* Blink the LED to show we're alive */
	while (1) {
		gpio_pin_write(dev, LED0_GPIO_PIN, 0);
		k_sleep(LED_BLINK_TIME);
		gpio_pin_write(dev, LED0_GPIO_PIN, 1);
		k_sleep(LED_INTERVAL_TIME - LED_BLINK_TIME);
	}
}
