MPEG TS Editor CLI Tool
===

This CLI (Command line interface) tool allows you to print your transport stream in hex format. 

You can view certain packets or bytes in hex format using the read mode.

You can also use the write mode to change certain bytes in the transport stream, just use the packet number / pid / byte position (in the 188-byte packet) as a filter to do your work.

## Table of Contents

* [Usage](#usage)
    * [Help](#help)
    * [Read a TS](#read-a-ts)
    * [Modify certain bytes in packets using filter](#modify-certain-bytes-in-packets-using-filter)

Usage
===

Help
---
`python tsEditor.py -h`

Read a TS
---
`python ./tsEditor.py -r -fp 36590 -tp 36600 -pid 64 -f Sample.ts`
<br>Sample output (1 packet with pid 64 from packet number 36590 to 36600):
![](https://github.com/kwanhiuhong/MPEG_TS_Modifier/blob/main/screenshots/read_1.png)
<br>

`python ./tsEditor.py -r -fp 36590 -tp 36600 -pid 48 -b 2 -f Sample.ts`
<br>Sample output (8 packets with pid 48 from packet number 36590 to 36600):
![](https://github.com/kwanhiuhong/MPEG_TS_Modifier/blob/main/screenshots/read_2.png)
<br>

Variable "numberOfBytesToRead" determine how many bytes the console will display, by default is 2.
![](https://github.com/kwanhiuhong/MPEG_TS_Modifier/blob/main/screenshots/read_3.png)
<br>

Modify certain bytes in packets using filter
---
Using the above as example, suppose there are originally 8 packets with pid 48 from packet 36590 to 36600. And now I would like to change these 8 packets' pid to 689. We first refer to MPEG TS standard to find out starting from what byte position should we start editing. As PID should be at byte position 2 in a 188 bytes packet. The hex format of "689" is 2B1. The first "0" is copied from the original packet such that current change will not distort the original ts. The new ts file will be named "<your_original_file_name>_output.ts", such that your original ts file will not be changed.

`python ./tsEditor.py -w -fp 36590 -tp 36600 -pid 48 -b 2 -nb "02B1" -f Sample.ts`
![](https://github.com/kwanhiuhong/MPEG_TS_Modifier/blob/main/screenshots/write_1.png)
<br>

Now, we can check by using the read mode. (Note that the new file is named as <original_file_name>_output.ts)
<br>`python ./tsEditor.py -r -fp 36590 -tp 36600 -pid 689 -b 2 -f Sample_output.ts`
![](https://github.com/kwanhiuhong/MPEG_TS_Modifier/blob/main/screenshots/write_2.png)
<br>
