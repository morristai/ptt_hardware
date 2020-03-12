# PTT_Crawler for HardwareSale

## Feature
- Auto cache newest index number, previous found items.
- Run on termux with crontab support.
- Auto send G-mail to notify when new item found.

## How to use
1. modify config.py to suit your case
2. run attached.py to start
3. if you want to auto schedule on Android, add this crontab script
```shell script
*/5 * * * * /data/data/com.termux/files/usr/bin/python /data/data/com.termux/files/home/storage/downloads/ptt_hardware-master/attached.py
```