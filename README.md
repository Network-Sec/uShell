# uShell
Universall Reverse and Bind Shell, encrypted, running over 443, evasive..

## WIP
Project just started, not nearly feature-complete.

## The Plan
Make something better than "nc -lvnp 9090" - instead a two-part, encrypted, evasive but still lightweight reverse shell / bind shell for everyday use:
- Keep it simple, no feature overflow
- Widely compatible, not relying on custom imports
- Maybe implant compiled to exe, elf, apk
- Support Linux, Windows and Android
- Focus on non-CTFy scenarios, real life applicability, where opsec is a factor (like using VPN) and we cant connect back, only forward
- Encrypt data stream. Simple encryption, but one that works, can be AES and password "your mom" as long as it's hidden from direct DPI and Logs
- Use standard ports like https and work more like a REST api that the implant queries / responds to on port 443, bypassing Firewalls (but still being essentially a good reverse shell), no detectable beacon traffic

Just a practical Offsec tool that's not directly flagged by the lowest instance of Windows 7 Defender and doesn't fail on real systems due to lack of X on the target. 

