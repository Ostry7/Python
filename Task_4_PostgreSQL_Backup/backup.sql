--
-- PostgreSQL database dump
--

\restrict alOyu9jpspLVoasPLkx2OIK1XwNS2aooGJtS0f8IYNq3pogslqaGkG6TZCzWVOG

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg12+1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.applications (
    id integer NOT NULL,
    app_name character varying(100),
    version character varying(20),
    servers_count integer,
    deployed_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.applications OWNER TO postgres;

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.applications_id_seq OWNER TO postgres;

--
-- Name: applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.applications_id_seq OWNED BY public.applications.id;


--
-- Name: backups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.backups (
    id integer NOT NULL,
    server_id integer,
    backup_size bigint,
    duration_ms integer,
    status character varying(20),
    s3_path character varying(500),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.backups OWNER TO postgres;

--
-- Name: backups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.backups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.backups_id_seq OWNER TO postgres;

--
-- Name: backups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.backups_id_seq OWNED BY public.backups.id;


--
-- Name: servers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servers (
    id integer NOT NULL,
    hostname character varying(100),
    ip_address inet,
    environment character varying(20),
    status character varying(20),
    cpu_usage numeric(5,2),
    memory_usage numeric(5,2),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.servers OWNER TO postgres;

--
-- Name: servers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.servers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.servers_id_seq OWNER TO postgres;

--
-- Name: servers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.servers_id_seq OWNED BY public.servers.id;


--
-- Name: applications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications ALTER COLUMN id SET DEFAULT nextval('public.applications_id_seq'::regclass);


--
-- Name: backups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backups ALTER COLUMN id SET DEFAULT nextval('public.backups_id_seq'::regclass);


--
-- Name: servers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servers ALTER COLUMN id SET DEFAULT nextval('public.servers_id_seq'::regclass);


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.applications (id, app_name, version, servers_count, deployed_at) FROM stdin;
1	nginx-web	1.25.3	15	2026-02-27 13:04:33.881548
2	nodejs-api	v20.11.0	8	2026-02-27 13:04:33.881548
3	postgres-db	16.2	3	2026-02-27 13:04:33.881548
\.


--
-- Data for Name: backups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.backups (id, server_id, backup_size, duration_ms, status, s3_path, created_at) FROM stdin;
1	1	1048576	2345	success	s3://devops-backups/web01-20260227.sql	2026-02-27 13:04:33.883515
2	2	5242880	15678	success	s3://devops-backups/db01-20260227.sql	2026-02-27 13:04:33.883515
3	3	102400	1234	failed	s3://devops-backups/app01-20260227.sql	2026-02-27 13:04:33.883515
\.


--
-- Data for Name: servers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servers (id, hostname, ip_address, environment, status, cpu_usage, memory_usage, created_at) FROM stdin;
1	web-01.prod.eu-west-1	10.0.1.10	production	running	12.50	45.30	2026-02-27 13:04:33.862854
2	db-01.prod.eu-west-1	10.0.1.20	production	maintenance	67.20	89.10	2026-02-27 13:04:33.862854
3	app-01.staging	10.0.2.30	staging	running	23.40	34.70	2026-02-27 13:04:33.862854
\.


--
-- Name: applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.applications_id_seq', 3, true);


--
-- Name: backups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.backups_id_seq', 3, true);


--
-- Name: servers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.servers_id_seq', 3, true);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: backups backups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backups
    ADD CONSTRAINT backups_pkey PRIMARY KEY (id);


--
-- Name: servers servers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servers
    ADD CONSTRAINT servers_pkey PRIMARY KEY (id);


--
-- Name: backups backups_server_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backups
    ADD CONSTRAINT backups_server_id_fkey FOREIGN KEY (server_id) REFERENCES public.servers(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO backup_user;


--
-- Name: TABLE applications; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.applications TO backup_user;


--
-- Name: SEQUENCE applications_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.applications_id_seq TO backup_user;


--
-- Name: TABLE backups; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.backups TO backup_user;


--
-- Name: SEQUENCE backups_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.backups_id_seq TO backup_user;


--
-- Name: TABLE servers; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.servers TO backup_user;


--
-- Name: SEQUENCE servers_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.servers_id_seq TO backup_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO backup_user;


--
-- PostgreSQL database dump complete
--

\unrestrict alOyu9jpspLVoasPLkx2OIK1XwNS2aooGJtS0f8IYNq3pogslqaGkG6TZCzWVOG

