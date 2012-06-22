#!/bin/python
import libtorrent as lt
import sys
import math

torrent = sys.argv[1]
info = lt.torrent_info(torrent)
#print info.num_pieces()
for f in info.files():
	off = float(f.offset)
	psize = info.piece_length()
	start = math.floor(off / psize)
	end = math.floor((off + f.size) / psize)
	print "%4d - %4d: %s" % (start, end, f.path)

