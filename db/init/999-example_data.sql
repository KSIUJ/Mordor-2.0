COPY public.tags (id, name) FROM stdin;
1	variable
2	algorithm
3	calculus
4	function
5	matrix
6	binary
7	array
8	boolean
9	theorem
10	integer
11	compile
12	structure
13	package
14	decimal
15	notation
\.

COPY public.users_limits (user_role, size_limit, number_limit) FROM stdin;
admin	89000000	38
user	9000000	10
X-role	45000000	16
\.

COPY public.users (id, username, role, email) FROM stdin;
1	jdixon	user	hwoodard@example.com
2	tgutierrez	user	xhubbard@example.net
3	shannondunlap	user	vjohnson@example.net
4	alicia90	admin	kristi27@example.com
5	chrisrhodes	user	heather33@example.org
6	yrivera	admin	nicolasramirez@example.net
7	hnewman	user	vernon22@example.net
8	qlopez	X-role	tylersara@example.com
9	jennifer74	X-role	fperez@example.net
10	khudson	X-role	josephramos@example.com
\.

COPY public.files (id, name, filepath, status, size, uploaded_at, uploaded_by) FROM stdin;
1	what.mp3	/uploads/what.mp3	rejected	7615039	2025-06-09 16:39:40	7
2	fine.bmp	/uploads/fine.bmp	accepted	6849018	2025-06-29 12:00:51	8
3	pull.flac	/uploads/pull.flac	rejected	1528738	2025-06-25 06:49:21	6
4	history.png	/uploads/history.png	rejected	8234067	2025-01-24 09:23:53	10
5	tree.mp3	/uploads/tree.mp3	accepted	1622514	2025-02-04 23:11:17	8
6	put.html	/uploads/put.html	pending	8509849	2025-04-30 08:51:31	7
7	someone.doc	/uploads/someone.doc	pending	7005587	2025-01-12 23:50:28	4
8	fish.css	/uploads/fish.css	rejected	5240994	2025-01-12 05:36:16	1
9	answer.wav	/uploads/answer.wav	accepted	6741545	2025-02-05 03:18:18	7
10	hard.flac	/uploads/hard.flac	rejected	2441737	2025-04-03 08:56:31	5
11	relationship.mov	/uploads/relationship.mov	accepted	2853434	2025-01-18 06:40:45	5
12	perhaps.webm	/uploads/perhaps.webm	rejected	377037	2025-07-30 19:07:58	7
13	throw.tiff	/uploads/throw.tiff	pending	3510903	2025-01-02 18:41:35	8
14	find.mov	/uploads/find.mov	rejected	1999799	2025-03-26 02:28:40	10
15	social.avi	/uploads/social.avi	accepted	8909485	2025-04-14 20:46:05	2
16	buy.png	/uploads/buy.png	rejected	3647063	2025-02-20 15:50:44	6
17	support.html	/uploads/support.html	pending	3471450	2025-07-18 13:38:50	7
18	provide.mp3	/uploads/provide.mp3	accepted	9099444	2025-06-26 18:22:18	10
19	up.webm	/uploads/up.webm	rejected	4920855	2025-01-18 11:02:35	4
20	another.css	/uploads/another.css	pending	9547435	2025-04-09 18:37:26	9
21	visit.tiff	/uploads/visit.tiff	pending	9088959	2025-03-24 22:08:49	4
22	expert.xls	/uploads/expert.xls	pending	9911846	2025-05-31 18:30:35	9
23	sense.bmp	/uploads/sense.bmp	accepted	5309729	2025-03-28 11:20:13	3
24	quite.jpeg	/uploads/quite.jpeg	accepted	4938840	2025-04-04 12:42:41	10
25	here.js	/uploads/here.js	pending	1283403	2025-03-21 05:39:21	3
26	agent.tiff	/uploads/agent.tiff	rejected	5470459	2025-01-11 06:15:15	8
27	natural.wav	/uploads/natural.wav	pending	7652446	2025-06-17 22:43:30	4
28	institution.gif	/uploads/institution.gif	rejected	8409761	2025-06-22 02:27:43	5
29	provide.txt	/uploads/provide.txt	accepted	3586479	2025-03-02 21:24:05	5
30	today.mp3	/uploads/today.mp3	rejected	6855144	2025-06-12 02:54:43	5
31	position.html	/uploads/position.html	accepted	155882	2025-02-04 05:54:26	6
32	need.png	/uploads/need.png	rejected	9157370	2025-07-27 11:53:36	7
33	nice.js	/uploads/nice.js	rejected	677141	2025-06-12 14:45:13	4
34	spend.mp4	/uploads/spend.mp4	accepted	3157363	2025-02-21 21:41:07	10
35	as.gif	/uploads/as.gif	pending	5549736	2025-03-26 06:52:41	7
36	turn.xls	/uploads/turn.xls	pending	6485576	2025-01-11 12:52:40	5
37	argue.mov	/uploads/argue.mov	accepted	3693287	2025-07-27 08:59:27	7
38	red.wav	/uploads/red.wav	accepted	8237457	2025-03-15 20:52:52	2
39	type.bmp	/uploads/type.bmp	rejected	6545655	2025-06-14 11:13:58	7
40	central.mov	/uploads/central.mov	accepted	7410667	2025-06-22 22:58:23	3
41	forward.css	/uploads/forward.css	pending	3237547	2025-07-20 11:16:23	6
42	food.wav	/uploads/food.wav	pending	214184	2025-07-08 21:30:36	4
43	prove.numbers	/uploads/prove.numbers	accepted	5345218	2025-05-08 05:58:45	1
44	assume.mov	/uploads/assume.mov	rejected	1653569	2025-04-26 21:19:37	6
45	until.html	/uploads/until.html	rejected	8526780	2025-06-19 09:46:29	7
46	model.mp3	/uploads/model.mp3	accepted	5181884	2025-05-16 10:28:26	9
47	attention.numbers	/uploads/attention.numbers	rejected	6273307	2025-01-07 17:25:24	6
48	main.mov	/uploads/main.mov	pending	7048106	2025-03-07 19:24:47	6
49	cultural.flac	/uploads/cultural.flac	rejected	273034	2025-03-07 00:04:19	4
50	once.jpg	/uploads/once.jpg	pending	8052140	2025-05-19 11:09:44	4
\.

COPY public.recently_opened (user_id, file_id, opened_at) FROM stdin;
1	35	2025-02-17 21:22:40
2	37	2025-02-15 06:17:59
4	18	2025-06-06 19:06:25
1	23	2025-06-22 13:59:57
7	1	2025-06-06 22:47:38
6	4	2025-02-23 04:38:11
10	26	2025-05-04 19:19:14
9	46	2025-04-04 14:15:19
8	8	2025-05-27 20:40:04
6	17	2025-05-29 01:24:36
5	33	2025-03-15 06:16:31
9	6	2025-03-15 22:11:12
2	49	2025-06-28 15:08:47
8	3	2025-01-22 01:49:26
9	9	2025-04-27 22:08:47
3	35	2025-03-18 22:00:05
8	10	2025-05-17 14:25:10
7	29	2025-01-23 18:58:22
9	44	2025-01-23 18:51:04
10	24	2025-05-25 15:37:30
7	12	2025-07-27 22:59:35
10	28	2025-06-20 21:54:33
5	5	2025-05-03 11:05:36
7	48	2025-02-10 00:15:07
10	42	2025-01-20 06:46:32
6	30	2025-04-22 01:08:43
5	14	2025-02-03 13:56:52
10	37	2025-06-23 02:12:44
7	24	2025-03-25 16:18:21
4	12	2025-04-03 02:41:39
7	34	2025-01-01 11:56:39
2	28	2025-07-29 12:34:23
1	26	2025-02-24 14:29:47
3	44	2025-01-10 04:02:17
1	45	2025-04-27 00:18:36
7	40	2025-03-24 04:56:49
6	29	2025-07-12 02:54:19
10	6	2025-03-31 00:32:51
5	28	2025-07-18 15:31:08
8	29	2025-01-20 04:26:42
\.

COPY public.tag_file (file_id, tag_id) FROM stdin;
1	5
1	13
2	11
2	3
3	7
3	2
4	10
4	14
5	12
5	4
6	4
6	1
7	9
7	11
8	3
8	5
9	7
9	12
10	2
10	6
11	11
11	9
12	11
12	4
13	6
13	7
14	12
14	13
15	10
15	15
16	6
16	15
17	15
17	5
18	4
18	8
19	10
19	5
20	12
20	11
21	1
21	5
22	11
22	13
23	10
23	12
24	1
24	8
25	7
25	12
26	12
26	7
27	8
27	2
28	13
28	2
29	5
29	12
30	13
30	3
31	3
31	1
32	14
32	1
33	11
33	14
34	9
34	13
35	10
35	7
36	4
36	9
37	10
37	3
38	7
38	3
39	6
39	12
40	12
40	10
41	2
41	12
42	7
42	1
43	9
43	15
44	3
44	15
45	11
45	8
46	7
46	8
47	8
47	15
48	1
48	4
49	11
49	9
50	8
50	15
\.