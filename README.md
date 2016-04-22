# MySis001
Sis001开车工具

Usage:
============


> * import SisDB.sql to your mysql;
> * modify mysql info in MySis001.py;
> * **drive** your car;

Command:
========

```python
python3 MySis001.py       #default, fetch 1-3 page
python3 MySis001.py 10    #fetch 1-10 page
python3 MySis001.py 2 10  #fetch 2-9 page
```


Crontab:
========
```shell
0 * * * * python3 $YOUR_PATH > /dev/null 2>&1
```