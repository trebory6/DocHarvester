Desktop Packages
Vikunja is available as an electron-based desktop application for Linux and Windows. For advanced desktop instructions, see the desktop README.
For end-user features — signing in, the quick-entry window, the system tray, and command-line flags — see the Desktop App help page.
Installation#
- Download the latest release for your platform from the download page.
- For Windows, choose the file with the
.exe
or.msi
file ending - For a Linux-based operating system, choose a file with an ending for your operating system - we have builds for Alpine, AppImage, Arch Linux, Debian-based systems, FreeBSD, Fedora and Snap.
- Run the downloaded package in the same way you would normally install a package for your OS.
> **Note**: If you’re self-hosting your Vikunja instance, you need to enable cors for at least the host http://127.0.0.1:45735
for the desktop application to work.
Flatpak#
Vikunja Desktop can be installed via the Flathub.
To install it, run the following command:
flatpak install flathub io.vikunja.Vikunja
