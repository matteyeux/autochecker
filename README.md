# autochecker
TSS check and save blobs automaticaly 
It's a work in progress script to automaticaly find a new version then save its SHSH blobs with Tihmstar's tsschecker

### Usage
`usage: ./autochecker.py [config file]`

Config file looks like this :
```
[device] iPhone5,4
[ecid] VVVVVVVVVV

[device] iPad2,5
[ecid] WWWWWWWWWWW

[device] iPhone8,1
[ecid] XXXXXXXXXXX

[device] iPad2,1
[ecid] YYYYYYYYYYY

[device] iPad2,1
[ecid] ZZZZZZZZZZZ

```

You can complete the file named `devices.sample` then use it with `autochecker` :
`./autochecker devices.sample`

Make sure [tsschecker](https://github.com/tihmstar/tsschecker) is installed in your PATH.

### TODO
- Add requirements.txt
- Add to crontab
