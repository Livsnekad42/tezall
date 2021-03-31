--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: affiliateLocs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."affiliateLocs" (
    id integer NOT NULL,
    "cityId" integer,
    "affiliateName" character varying(255),
    "affiliatePhone" character varying(255),
    address character varying(255),
    schedule character varying(255),
    latitude character varying(255),
    longitude character varying(255),
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."affiliateLocs" OWNER TO postgres;

--
-- Name: affiliateLocs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."affiliateLocs_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."affiliateLocs_id_seq" OWNER TO postgres;

--
-- Name: affiliateLocs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."affiliateLocs_id_seq" OWNED BY public."affiliateLocs".id;


--
-- Name: cityLocs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."cityLocs" (
    id integer NOT NULL,
    "cityName" character varying(255),
    latitude character varying(255),
    longitude character varying(255),
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."cityLocs" OWNER TO postgres;

--
-- Name: cityLocs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."cityLocs_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."cityLocs_id_seq" OWNER TO postgres;

--
-- Name: cityLocs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."cityLocs_id_seq" OWNED BY public."cityLocs".id;


--
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comments (
    id integer NOT NULL,
    project character varying(200),
    username character varying(200),
    content character varying(500),
    avatar character varying(500),
    "cityId" integer,
    "isPublic" boolean,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.comments OWNER TO postgres;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_id_seq OWNER TO postgres;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    title character varying(500),
    alias character varying(500),
    url character varying(500),
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documents_id_seq OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(255),
    email character varying(255),
    password character varying(255) DEFAULT false,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: affiliateLocs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."affiliateLocs" ALTER COLUMN id SET DEFAULT nextval('public."affiliateLocs_id_seq"'::regclass);


--
-- Name: cityLocs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."cityLocs" ALTER COLUMN id SET DEFAULT nextval('public."cityLocs_id_seq"'::regclass);


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: affiliateLocs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."affiliateLocs" (id, "cityId", "affiliateName", "affiliatePhone", address, schedule, latitude, longitude, "createdAt", "updatedAt") FROM stdin;
2	1	НурЖол	+7 (707) 443-43-34	Сарыаркинский район ул. Богенбай-батыра д. 89	09:00 21:00	51.170646	71.415071	2020-08-12 11:05:29.689+06	2020-08-12 11:05:29.689+06
3	2	Мерей	+7 (771) 022-69-29	 пр. Суюнбая, д. 2, ТД "Мерей", бутик №15, вход со стороны улицы	10:00-20:00	43.273906	76.947168	2020-08-12 11:24:29.668+06	2020-08-12 11:28:05.549+06
1	1	ТД Артем	+7 (771) 022-69-01	 ул. Сакена Сейфуллина, д. 27, ТД "Артем", 2 этаж, бутик 154/2	10:00-22:00	51.171269	71.421200	2020-08-12 11:02:53.651+06	2020-08-12 11:30:05.422+06
4	\N	Капшагай	+7 (771) 022-69-40	г. Капшагай, 4 микрорайон, д. 23	9:00-17:00	43.852382	77.054938	2020-08-19 14:04:59.055+06	2020-08-19 14:04:59.055+06
5	4	Сырымбет	+7 (771) 022-69-37	мкр.Васильковского 34,ТД "Сырымбет"	9:00 -17:00	53.311469	69.391056	2020-08-19 14:13:46.375+06	2020-08-19 14:13:46.375+06
6	3	Капшагай	+7 (771) 022-69-40	г. Капшагай, 4 микрорайон, д. 23	9:00 -17:00	43.852382	77.054938	2020-08-19 14:15:07.799+06	2020-08-19 14:15:07.799+06
7	5	Ауыл Береке	+7 (771) 022-69-35	Ауыл Береке	9:00 -17:00	42.909167	71.412283	2020-08-19 14:32:32.012+06	2020-08-19 14:32:32.012+06
8	5	Диана	+7 (771) 022-69-33	Б.Момышулы 18 , кв. 9, ТД "Диана"	9:00 -17:00	42.895688	71.329198	2020-08-19 14:33:11.404+06	2020-08-19 14:33:11.404+06
9	6	Оптика	+7 (771) 022-69-31	ул. Биржан Сал 80	9:00 -17:00	45.019150	78.377227	2020-08-19 14:34:42.982+06	2020-08-19 14:34:42.982+06
10	6	Еркин	+7 (771) 022-69-32	ул. Биржан Сал 62, ТД "ЕРКИН"	9:00 -17:00	45.021755	78.377146	2020-08-19 14:35:29.661+06	2020-08-19 14:35:29.661+06
11	2	Оптовка	+7 (771) 022-69-29	 ул. Розыбакиева 33/1, бутик 44	9:00 -17:00	43.256364	76.886895	2020-08-19 14:36:13.938+06	2020-08-19 14:36:13.938+06
12	2	Водник	+7 (771) 022-69-39	г. Алматы, Илийский район, село Боралдай , Мкр. Водник, ул. Алатау , д. 2, 6 ряд, 1 Бутик	9:00 -17:00	43.368621	76.861520	2020-08-19 14:37:45.2+06	2020-08-19 14:37:45.2+06
13	2	Шолохова	+7 (771) 022-69-42	ул. Шолохова, д. 4А	9:00 -17:00	43.333279	76.955194	2020-08-19 14:38:40.448+06	2020-08-19 14:38:40.448+06
14	2	Тастак	+7 (771) 022-69-26	ул. Толе Би, д. 262	9:00 -17:00	43.249831	76.878334	2020-08-19 14:39:36.949+06	2020-08-19 14:39:36.949+06
15	1	ТД Артем	+7 (771) 022-69-01	ул. Сакена Сейфуллина, д. 47, ТД "Артем", 2 этаж, бутик 154/2	9:00 -17:00	51.173332	71.436717	2020-08-19 14:41:06.507+06	2020-08-19 14:41:06.507+06
16	1	Центральный рынок	+7 (771) 022-69-11	Алаш шоссе, 15/1, Сектор блок 4, Место 166	9:00 -17:00	51.195260	71.466658	2020-08-19 14:41:54.435+06	2020-08-19 14:41:54.435+06
17	1	ТД Береке	+7 (771) 022-69-02	мкр. Промышленный (Силикатный),ул. Шалкөде, 2А, ТД "Береке", 1 этаж	9:00 -17:00	51.122757	71.522075	2020-08-19 14:42:34.862+06	2020-08-19 14:42:34.862+06
18	1	ТД Гульжан	+7 (771) 022-69-06	пр. Абылай хана, 34, ТД "Гульжан" (новый), 1 этаж, бутик 109Б	9:00 -17:00	51.153620	71.485271	2020-08-19 14:43:16.003+06	2020-08-19 14:43:16.003+06
19	1	ТД Алем	+7 (771) 022-69-00	пр. Богенбай Батыра 62, ТД "АЛЕМ", 2 этаж, Ломбардный двор, бутик 10	9:00 -17:00 (по пн.сан.день)	51.177816	71.435550	2020-08-19 14:44:15.755+06	2020-08-19 14:44:15.755+06
20	1	ТД Северный	+7 (771) 022-69-13	ул. Косшыгулулы, 9, ТД "Солтүстік" (Северный), 1 этаж, бутик №109	9:00 -17:00	51.168628	71.389367	2020-08-19 14:44:52.78+06	2020-08-19 14:44:52.78+06
21	1	Евразия	+7 (771) 022-69-17	ул. Петрова, д. 17, 1 этаж, напротив ТЦ "Евразия"	9:00 -17:00	51.149456	71.471060	2020-08-19 14:45:27.82+06	2020-08-19 14:45:27.82+06
22	1	Победа	+7 (771) 022-69-22	пр. Жеңіс (Победы), д. 73, за остановкой, рядом маг. "Яблочко"	9:00 -17:00	51.187606	71.407315	2020-08-19 14:46:04.729+06	2020-08-19 14:46:04.729+06
23	1	Лесная поляна	+7 (771) 022-69-53	мкр. Лесная поляна, д. 9, пом. 17	9:00 -17:00	51.001045	71.376000	2020-08-19 14:46:39.061+06	2020-08-19 14:46:39.061+06
\.


--
-- Data for Name: cityLocs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."cityLocs" (id, "cityName", latitude, longitude, "createdAt", "updatedAt") FROM stdin;
3	Капшагай	43.8669688	77.0355997	2020-08-19 14:05:50.837+06	2020-08-19 14:12:28.421+06
5	Тараз	42.8961119	71.2988213	2020-08-19 14:16:33.531+06	2020-08-19 14:16:33.531+06
6	Талдыкорган	45.0105495	78.354835	2020-08-19 14:34:00.735+06	2020-08-19 14:34:00.735+06
1	Нур-Султан	51.1801000	71.4459800	2020-08-12 11:00:27.045+06	2020-11-29 17:04:01.922+06
2	Алматы	43.225638	76.881813	2020-08-12 11:10:57.697+06	2020-11-29 22:16:19.961+06
4	Кокшетау	53.298087	69.3380369	2020-08-19 14:11:22.347+06	2020-11-30 10:42:11.617+06
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comments (id, project, username, content, avatar, "cityId", "isPublic", "createdAt", "updatedAt") FROM stdin;
7	tezAqsha	dfgdf	sdfsdfsdf		3	f	2020-12-30 13:47:02.757+06	2020-12-30 14:01:43.779+06
8	tezAqsha	йцукйцук	йцукйцукйцукйцукйцукуйц		3	f	2020-12-30 13:57:14.386+06	2020-12-30 14:01:45.697+06
13	tezAqsha	qweqwe	xvbdfvbvfbvcv		3	f	2021-01-06 09:42:36.817+06	2021-01-06 09:42:36.817+06
2	tezAqsha	Индира	Сотрудники ТезКредит обслуживают вежливо и быстро. Оформила займ на точке за 10 минут и пошла с наличными домой!	src/img/about/photo.png	6	t	2020-12-28 16:33:07.806+06	2021-01-08 14:42:02.967+06
9	tezAqsha	Артем	Текст отзыва	src/img/about/photo.png	2	t	2020-12-30 14:04:37.001+06	2021-01-08 17:09:46.042+06
\.


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents (id, title, alias, url, "createdAt", "updatedAt") FROM stdin;
12	Договор	dogovor	/media/Dogovor_okazaniya_uslug.pdf	2020-12-25 11:59:54.821+06	2020-12-25 11:59:54.821+06
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, "createdAt", "updatedAt") FROM stdin;
1	Admin	tez_admin@gmail.com	$2a$08$tWCXLrtwiZkLac6fgBfdDOehJOdMPyKON1S/pLw3O.ca1UmqZISPm	2020-08-12 10:58:36.935+06	2020-08-12 10:58:36.935+06
\.


--
-- Name: affiliateLocs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."affiliateLocs_id_seq"', 23, true);


--
-- Name: cityLocs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."cityLocs_id_seq"', 6, true);


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comments_id_seq', 14, true);


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_id_seq', 12, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: affiliateLocs affiliateLocs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."affiliateLocs"
    ADD CONSTRAINT "affiliateLocs_pkey" PRIMARY KEY (id);


--
-- Name: cityLocs cityLocs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."cityLocs"
    ADD CONSTRAINT "cityLocs_pkey" PRIMARY KEY (id);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: affiliateLocs affiliateLocs_cityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."affiliateLocs"
    ADD CONSTRAINT "affiliateLocs_cityId_fkey" FOREIGN KEY ("cityId") REFERENCES public."cityLocs"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: comments comments_cityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT "comments_cityId_fkey" FOREIGN KEY ("cityId") REFERENCES public."cityLocs"(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

