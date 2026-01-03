# mp3p-revival

<div align="center">
Revival server for the Metroid Prime 3 Preview channel.
<br><br>
<img src="https://img.idkwh.ct8.pl/mp3p-revival/1.png" width="311" height="299" alt="image" />
</div>

## Prepatched WAD

A hosted WAD is available below:

- [European Version](https://img.idkwh.ct8.pl/mp3p-revival/wad/Metroid%20Prime%203%20Revival%20%28Europe%29%20%28Revival%29.wad) (might not have every video in every language)

- [American Version](https://img.idkwh.ct8.pl/mp3p-revival/wad/Metroid%20Prime%203%20Revival%20%28USA%29%20%28Revival%29.wad)

<small>All videos used are from YouTube</small>

## Self hosting

Install the requirements

```bash
pip install -r requirements.txt
```

Then run

```bash
py server.py
```

## WAD Patching

1. _Legally_ dump your own copy of the Metroid Prime 3 Preview channel
2. Unpack the WAD using WADMii or ShowMiiWADs
3. Unpack `00000002.app` using U8Mii or ShowMiiWADs
4. Decompress the DOL (`00000001.app`) using [wwcxtool](https://repo.mariocube.com/Wii/PC%20Applications/WAD%20Tools/wwcxtool.zip)
5. Open the DOL, and modify the URL
    - The URL in the European WAD is located at offset `0x223E10`
    - The URL in the American WAD is located at offset `0x223928`
    - Optionally, recompress the DOL using wwcxtool.
6. Open `html.arc` found in `00000002.app`, modify the first line of `video.js` to your custom URL, then repack the U8 archive. ([CTools's SZS Explorer](https://www.chadsoft.co.uk/wiicoder/) is recommended)
7. Repack the WAD
8. If done correctly, it should be pointing to your custom `videos.txt`.

## Adding custom videos

The channel simply uses .mp4 in a .3gp container, with a max resolution of 240p (max. tested: 15fps), to encode videos correctly, you need [ffmpeg](https://ffmpeg.org/).

Encode a video to a supported .mp4

```bash
ffmpeg -i input.mp4 -vf scale=320:240,setsar=1,fps=15 -c:v libx264 -profile:v baseline -level 1.1 -pix_fmt yuv420p -x264-params "cabac=0:ref=1:bframes=0:weightp=0:8x8dct=0:scenecut=0:vbv-maxrate=300:vbv-bufsize=300:nal-hrd=none:aud=0:repeat-headers=1" -colorspace bt470bg -color_primaries bt470bg -color_trc smpte170m -g 30 -keyint_min 30 -c:a aac -ar 32000 -ac 2 -b:a 96k -movflags +faststart output.mp4
```

To convert the output to .3gp

```bash
ffmpeg -i output.mp4 -c copy -movflags +faststart output.3gp
```

Then place the final 3gp to `/videos/`, you might need to rename the file to whatever the channel accepts (`1-11.3gp` for Europe, `1-10.3gp` for USA)

## Troubleshooting

1. I get an error (-1022,-1029) when I try to install the WAD on real hardware
    - Uninstall the WAD, then install it again

2. Sometimes, the channel crashes with the death sound
    - Unfortunately, the channel is a browser (Opera) app, and it might sometimes crash.
