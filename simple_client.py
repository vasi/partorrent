#!/bin/python
# Copyright Arvid Norberg 2008. Use, modification and distribution is
# subject to the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)


import libtorrent as lt
import time
import signal
import string
import sys

torrent = sys.argv[1]
pieces = sys.argv[2] if len(sys.argv) > 2 else '*'

resume_file = '.fastresume'
ses = lt.session()
ses.listen_on(6881, 6891)

info = lt.torrent_info(torrent)
params = {'ti': info, 'save_path': './', 'paused': True}
try:
	params['resume_data'] = open(resume_file, 'rb').read()
except:
	pass
h = ses.add_torrent(params)

np = info.num_pieces()
prios = [0] * np
for r in string.split(pieces, ','):
	first, last = 0, np - 1
	if string.strip(r) != '*':
		ends = string.split(r, '-')
		if len(ends) == 1:
			first = last = int(r)
		elif len(ends) == 2:
			a, b = ends
			first = int(a) if string.strip(a) != '' else first
			last = int(b) if string.strip(b) != '' else last
		else:
			raise Exception("bad range")
	if first < 0:
		first = 0
	if last >= np:
		last = np - 1
	for i in range(first, last + 1):
		prios[i] = 7
h.prioritize_pieces(prios)

h.resume()
print 'starting', h.name()

done = [False] # how i wish for non-local
def interrupt(signum, frame):
	done[0] = True
signal.signal(signal.SIGINT, interrupt)
while not done[0]:
	s = h.status()
	state_str = ['queued', 'checking', 'downloading metadata', \
		'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
	print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
		(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
		s.num_peers, state_str[s.state]),
	sys.stdout.flush()

	time.sleep(1)
	done[0] = done[0] or h.is_finished()

open(resume_file, 'wb').write(lt.bencode(h.write_resume_data()))
print h.name(), 'complete'

