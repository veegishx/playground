#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import libtools
from pisi.actionsapi import texlivemodules

import os

WorkDir = "."

def setup():
    if get.ARCH() == "x86_64":
        shelltools.export("CFLAGS", "%s -fPIC" % get.CFLAGS())

    shelltools.cd("/%s/source/" % get.workDIR())

    # prevent compiling Xdvi with libXp
    # it's a workaround should be fixed with a better regex pattern
    pisitools.dosed("texk/xdvik/configure","-lXp ")

    shelltools.makedirs("%s/source/build" % get.workDIR())
    shelltools.cd("%s/source/build" % get.workDIR())

    shelltools.sym("../configure", "configure")
    autotools.configure("--disable-native-texlive-build \
                         --with-banner-add=\"/PisiLinux\" \
                         --disable-multiplatform \
                         --disable-chktex \
                         --disable-dialog \
                         --disable-detex \
                         --disable-dvipng \
                         --disable-dvi2tty \
                         --disable-dvipdfmx \
                         --disable-lcdf-typetools \
                         --disable-ps2eps \
                         --disable-psutils \
                         --disable-t1utils \
                         --disable-bibtexu \
                         --disable-xz \
                         --disable-xdvik \
                         --enable-shared \
                         --disable-static \
                         --with-system-zlib \
                         --with-system-icu \
                         --with-system-pnglib \
                         --with-system-ncurses \
                         --with-system-t1lib \
                         --with-system-gd \
                         --with-system-xpdf \
                         --with-system-poppler \
                         --with-system-cairo \
                         --with-system-freetype2 \
                         --with-system-harfbuzz \
                         --with-system-graphite2 \
                         --with-freetype2-libdir=/usr/lib \
                         --with-freetype2-include=/usr/include/freetype2 \
                         --with-xdvi-x-toolkit=xaw \
                         --disable-dump-share \
                         --disable-aleph \
                         --disable-luatex \
                         --with-clisp-runtime=default \
                         --enable-xindy --disable-xindy-rules --disable-xindy-docs")

def build():
    shelltools.cd("%s/source/build" % get.workDIR())
    autotools.make()

def install():
    folders = ["/usr/share",
               "/etc/texmf/web2c",
               "/etc/texmf/chktex",
               "/etc/texmf/dvips/config",
               "/etc/texmf/dvipdfm/config",
               "/etc/texmf/dvipdfmx",
               "/etc/texmf/tex/generic/config",
               "/etc/texmf/ttf2pk",
               "/etc/texmf/xdvi",
               "/etc/fonts/conf.avail"]

    for dirs in folders:
        pisitools.dodir(dirs)
        
    pisitools.insinto("/etc/fonts/conf.avail/", "09-texlive-fonts.conf")
    
    # copy config files to $TEXMFSYSCONFIG tree (defined in texmf.cnf)
    config_files = [ "/usr/share/texmf/chktex/chktexrc",
                     "/usr/share/texmf/web2c/mktex.cnf",
                     "/usr/share/texmf/web2c/updmap.cfg",
                     "/usr/share/texmf/web2c/fmtutil.cnf",
                     "/usr/share/texmf/dvips/config/config.ps",
                     "/usr/share/texmf/dvipdfmx/dvipdfmx.cfg",
                     "/usr/share/texmf/tex/generic/config/pdftexconfig.tex",
                     "/usr/share/texmf/tex/generic/config/language.dat",
                     "/usr/share/texmf/tex/generic/config/language.def",
                     "/usr/share/texmf/ttf2pk/ttf2pk.cfg",
                     "/usr/share/texmf/xdvi/XDvi"]

    for share_file in config_files:
        etc_file = share_file.replace("/usr/share", "/etc")
        shelltools.copy("%s/%s" % (get.installDIR(), share_file) , "%s/%s" % (get.installDIR(), etc_file))
    
    #make install
    shelltools.cd("%s/source/build" % get.workDIR()) 
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
        # remove symlinks to scripts that are not in texlive-bin or texlive-core:
    symlinks_to_remove = ["authorindex",
                          "ebong",
                          "bibexport",
                          "cachepic",
                          "epspdf",
                          "epspdftk",
                          "fig4latex",
                          "makeglossaries",
                          "mathspic",
                          "mkgrkindex",
                          "pdfannotextractor",
                          "perltex",
                          "pst2pdf",
                          "ps4pdf",
                          "splitindex",
                          "svn-multi",
                          "htcontext",
                          "htlatex",
                          "htmex",
                          "ht",
                          "httexi",
                          "httex",
                          "htxelatex",
                          "htxetex",
                          "mk4ht",
                          "ulqda",
                          "vpe",
                          "tlmgr"]

    for symlink in symlinks_to_remove:
        pisitools.remove("/usr/bin/%s" % symlink)
