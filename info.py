#!/usr/bin/env python
# Copyright Dave Vasilevsky 2012
import libtorrent as lt
import sys
import math

torrent = sys.argv[1]
info = lt.torrent_info(torrent)
print "Pieces: %d" % info.num_pieces()
print "Piece size: %d K" % (info.piece_length() / 1024)
for f in info.files():
	off = float(f.offset)
	psize = info.piece_length()
	start = off / psize
	print "%7.2f: %s" % (start, f.path)

