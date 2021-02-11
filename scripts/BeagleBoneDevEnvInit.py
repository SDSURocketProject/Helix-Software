import os
import urllib.request
import argparse
import apt

if __name__ == "__main__":
    aptPackagesToInstall = ["tar", "git", "build-essential", "doxygen", "clang-format", "texlive-xetex", "texlive-fonts-recommended"]
    pip3PackagesToInstall = ["numpy", "matplotlib", "sphinx"]
    
    precompiledBoostArmurl = "http://elon.sdsurocketproject.org/wikistatic/BeagleBoneSetup/boost_1_72_0_arm.tar.gz"
    precompiledBoostx86url = "http://elon.sdsurocketproject.org/wikistatic/BeagleBoneSetup/boost_1_72_0_x86.tar.gz"
    precompiledGCCArm = "http://elon.sdsurocketproject.org/wikistatic/BeagleBoneSetup/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf.tar.xz"

    parser = argparse.ArgumentParser(description="Setup dev environment expected by the build scripts for the helix-software project.")
    parser.add_argument("--install-directory", help="Specify a different install directory from the default of \'/opt/helix-software-tools\'.", default="/opt/helix-software-tools", nargs=1)
    parser.add_argument('--skip-install-dependencies', help="Skip installing dependencies for the build system.", action="store_true")
    parser.add_argument('--skip-install-dev-tools', help="Skip installing boost libraries and gcc arm toolchain.", action="store_true")

    args = parser.parse_args()    

    if (os.getuid() != 0):
        print("This init script requires root to run apt-get to install required dependencies.")
        print("Rerun this script as root or use the argument --skip-install-dependencies to skip installing dependencies.")
        exit(1)
    
    # Install apt-get packages
    if (args.skip_install_dependencies == False):
        cache = apt.cache.Cache()
        cache.update()
        cache.open()
        for package in aptPackagesToInstall:
            pkg = cache[package]
            if pkg.is_installed:
                print(f"{package} already installed.")
            else:

                print(f"Installing {package}...")
                os.system(f"apt-get -yq install {package}")
        
        for package in pip3PackagesToInstall:
            print(f"Installing python3 {package}...")
            os.system(f"pip3 -q install {package}")
        
        print("")
    
    installDir = os.path.normpath(args.install_directory)

    if (args.skip_install_dev_tools == False):
        # Create directories for dev tools
        try:
            print("Creating folder for development tools...")
            os.makedirs(installDir)
        except OSError as err:
            if (err.errno != os.errno.EEXIST):
                raise
        
        # Downlaod dev tools
        archivesToInstall = {
            f"Installing precompiled boost v1.72 for ARM to \'{installDir}\'...":"http://elon.sdsurocketproject.org/wikistatic/BeagleBoneSetup/boost_1_72_0_arm.tar.gz",
            f"Downloading precompiled boost v1.72 for x86 to \'{installDir}\'...":"http://elon.sdsurocketproject.org/wikistatic/BeagleBoneSetup/boost_1_72_0_x86.tar.gz",
            f"Downloading precompiled gcc toolchain for ARM to \'{installDir}\'...":"http://elon.sdsurocketproject.org/wikistatic/BeagleBoneSetup/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf.tar.xz"
        }
        
        testFileLocal = "temp_archive.tar.gz"
        for item in archivesToInstall:
            print(item)
            print("Downloading archive to temporary archive")
            urllib.request.urlretrieve(archivesToInstall[item], installDir+'/'+testFileLocal)
        
            print("Untaring temporary archive")
            os.system(f"tar xf {installDir+'/'+testFileLocal} -C {installDir}")
            print("Deleting temporary archive")
            os.remove(installDir+'/'+testFileLocal)
            print("")
        os.system("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/helix-software-tools/boost_1_72_0_x86/stage/lib")
    print("Finished initializing dev environment for helix-software without error.")
