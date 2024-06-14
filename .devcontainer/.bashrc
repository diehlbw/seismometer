#Override the default prompt, colorize $
PS1='${debian_chroot:+($debian_chroot)}\h:\w\[\033[1;36m\]$ \[\033[00m\]'

export PATH=$PATH:$HOME/.local/bin
