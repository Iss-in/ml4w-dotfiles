#!/bin/bash
sleep 1

_runUpdate() {
    case $install_platform in
        arch)
<<<<<<< HEAD
            bash <(curl -s https://raw.githubusercontent.com/quack-o/ml4w-dotfiles/main/setup-arch.sh)
        ;;
        fedora)
            bash <(curl -s https://raw.githubusercontent.com/quack-o/ml4w-dotfiles/main/setup-fedora.sh)
        ;;
=======
            bash <(curl -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles/main/setup-arch.sh)
            ;;
        fedora)
            bash <(curl -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles/main/setup-fedora.sh)
            ;;
>>>>>>> 7d5a2de47aeff048cbcd0006fe599d4c8b040f37
        CANCEL)
            _writeCancel
            exit
            ;;
        *)
            _writeCancel
            exit
            ;;
    esac
}

_runUpdate
