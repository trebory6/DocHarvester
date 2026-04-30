Build Vikunja from sources
To fully build Vikunja from source files, you need to build the api and frontend.
General Preparations#
- Make sure you have git installed
- Clone the repo with
git clone https://code.vikunja.io/vikunja
and switch into the directory. - Check out the version you want to build with
git checkout VERSION
- replaceVERSION
with the version you want to use. If you don’t do this, you’ll build the latest unstable build, which might contain bugs.
Frontend#
The code for the frontend is located in the frontend/
sub folder of the main repo.
- Make sure you have pnpm properly installed on your system.
- Install all dependencies with
pnpm install
- Build the frontend with
pnpm run build
. This will result in a static js bundle in thedist/
folder. - You can either deploy that static js bundle directly, or read on to learn how to bundle it all up in a static binary with the api.
API#
The Vikunja API has no other dependencies than go itself. That means compiling it boils down to these steps:
- Make sure Go is properly installed on your system. You’ll need at least Go
1.21
. - Make sure Mage is properly installed on your system.
- If you did not build the frontend in the steps before, you need to either do that or create a dummy index file with
mkdir -p frontend/dist && touch frontend/dist/index.html
. - Run
mage build
in the source of the main repo. This will build a binary in the root of the repo which will be able to run on your system.
Build for different architectures#
To build for other platforms and architectures than the one you’re currently on, simply run mage release
or mage release:{linux|windows|darwin}
.
More options are available, please refer to the magefile docs for more details.
