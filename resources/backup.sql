--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

-- Started on 2025-08-07 03:02:33

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 400660)
-- Name: activity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity (
    name text NOT NULL,
    parent_id uuid,
    level integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.activity OWNER TO postgres;

--
-- TOC entry 4824 (class 0 OID 0)
-- Dependencies: 216
-- Name: COLUMN activity.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.activity.name IS 'Название деятельности';


--
-- TOC entry 4825 (class 0 OID 0)
-- Dependencies: 216
-- Name: COLUMN activity.parent_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.activity.parent_id IS 'Родительская деятельность';


--
-- TOC entry 4826 (class 0 OID 0)
-- Dependencies: 216
-- Name: COLUMN activity.level; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.activity.level IS 'Уровень вложенности (1-3)';


--
-- TOC entry 4827 (class 0 OID 0)
-- Dependencies: 216
-- Name: COLUMN activity.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.activity.created_at IS 'Дата создания';


--
-- TOC entry 215 (class 1259 OID 400655)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 400672)
-- Name: building; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.building (
    address text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    created_at timestamp with time zone NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.building OWNER TO postgres;

--
-- TOC entry 4828 (class 0 OID 0)
-- Dependencies: 217
-- Name: COLUMN building.address; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.building.address IS 'Адрес здания';


--
-- TOC entry 4829 (class 0 OID 0)
-- Dependencies: 217
-- Name: COLUMN building.latitude; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.building.latitude IS 'Широта';


--
-- TOC entry 4830 (class 0 OID 0)
-- Dependencies: 217
-- Name: COLUMN building.longitude; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.building.longitude IS 'Долгота';


--
-- TOC entry 4831 (class 0 OID 0)
-- Dependencies: 217
-- Name: COLUMN building.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.building.created_at IS 'Дата создания';


--
-- TOC entry 218 (class 1259 OID 400679)
-- Name: organization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization (
    name text NOT NULL,
    building_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.organization OWNER TO postgres;

--
-- TOC entry 4832 (class 0 OID 0)
-- Dependencies: 218
-- Name: COLUMN organization.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization.name IS 'Название организации';


--
-- TOC entry 4833 (class 0 OID 0)
-- Dependencies: 218
-- Name: COLUMN organization.building_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization.building_id IS 'Здание';


--
-- TOC entry 4834 (class 0 OID 0)
-- Dependencies: 218
-- Name: COLUMN organization.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization.created_at IS 'Дата создания';


--
-- TOC entry 219 (class 1259 OID 400691)
-- Name: organization_activity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization_activity (
    organization_id uuid NOT NULL,
    activity_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.organization_activity OWNER TO postgres;

--
-- TOC entry 4835 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN organization_activity.organization_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization_activity.organization_id IS 'Организация';


--
-- TOC entry 4836 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN organization_activity.activity_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization_activity.activity_id IS 'Деятельность';


--
-- TOC entry 4837 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN organization_activity.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization_activity.created_at IS 'Дата создания';


--
-- TOC entry 220 (class 1259 OID 400706)
-- Name: organization_phone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization_phone (
    organization_id uuid NOT NULL,
    phone_number text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.organization_phone OWNER TO postgres;

--
-- TOC entry 4838 (class 0 OID 0)
-- Dependencies: 220
-- Name: COLUMN organization_phone.organization_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization_phone.organization_id IS 'Организация';


--
-- TOC entry 4839 (class 0 OID 0)
-- Dependencies: 220
-- Name: COLUMN organization_phone.phone_number; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization_phone.phone_number IS 'Номер телефона';


--
-- TOC entry 4840 (class 0 OID 0)
-- Dependencies: 220
-- Name: COLUMN organization_phone.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.organization_phone.created_at IS 'Дата создания';


--
-- TOC entry 4814 (class 0 OID 400660)
-- Dependencies: 216
-- Data for Name: activity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activity (name, parent_id, level, created_at, id) FROM stdin;
Еда	\N	1	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440101
Автомобили	\N	1	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440102
Мясная продукция	550e8400-e29b-41d4-a716-446655440101	2	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440103
Молочная продукция	550e8400-e29b-41d4-a716-446655440101	2	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440104
Грузовые	550e8400-e29b-41d4-a716-446655440102	2	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440105
Легковые	550e8400-e29b-41d4-a716-446655440102	2	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440106
Запчасти	550e8400-e29b-41d4-a716-446655440106	3	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440107
Аксессуары	550e8400-e29b-41d4-a716-446655440106	3	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440108
\.


--
-- TOC entry 4813 (class 0 OID 400655)
-- Dependencies: 215
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
065d0ff6387b
\.


--
-- TOC entry 4815 (class 0 OID 400672)
-- Dependencies: 217
-- Data for Name: building; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.building (address, latitude, longitude, created_at, id) FROM stdin;
г. Москва, ул. Ленина 1, офис 3	55.7522	37.6156	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440001
г. Москва, ул. Блюхера 32/1	55.7937	37.5501	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440002
г. Москва, ул. Тверская 7	55.7577	37.6097	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440003
\.


--
-- TOC entry 4816 (class 0 OID 400679)
-- Dependencies: 218
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization (name, building_id, created_at, id) FROM stdin;
ООО Рога и Копыта	550e8400-e29b-41d4-a716-446655440001	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440201
ЗАО Молоко	550e8400-e29b-41d4-a716-446655440002	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440202
АвтоМир	550e8400-e29b-41d4-a716-446655440003	2025-08-05 17:27:00+03	550e8400-e29b-41d4-a716-446655440203
\.


--
-- TOC entry 4817 (class 0 OID 400691)
-- Dependencies: 219
-- Data for Name: organization_activity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization_activity (organization_id, activity_id, created_at, id) FROM stdin;
550e8400-e29b-41d4-a716-446655440201	550e8400-e29b-41d4-a716-446655440103	2025-08-05 17:27:00+03	019881d5-364a-78aa-8f53-059b0000fffa
550e8400-e29b-41d4-a716-446655440201	550e8400-e29b-41d4-a716-446655440104	2025-08-05 17:27:00+03	019881d5-364b-795b-b9a8-d8992c69446e
550e8400-e29b-41d4-a716-446655440202	550e8400-e29b-41d4-a716-446655440104	2025-08-05 17:27:00+03	019881d5-364c-711d-a7df-516744ac28c3
550e8400-e29b-41d4-a716-446655440203	550e8400-e29b-41d4-a716-446655440107	2025-08-05 17:27:00+03	019881d5-364d-7439-8e55-b5a40756d0eb
550e8400-e29b-41d4-a716-446655440203	550e8400-e29b-41d4-a716-446655440108	2025-08-05 17:27:00+03	019881d5-364e-7bc4-97ed-d29b2733699e
\.


--
-- TOC entry 4818 (class 0 OID 400706)
-- Dependencies: 220
-- Data for Name: organization_phone; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization_phone (organization_id, phone_number, created_at, id) FROM stdin;
550e8400-e29b-41d4-a716-446655440201	2-222-222	2025-08-05 17:27:00+03	019881d5-3640-75a0-b391-ab803627e6ac
550e8400-e29b-41d4-a716-446655440201	3-333-333	2025-08-05 17:27:00+03	019881d5-3641-7dc5-9b42-1e86c980e544
550e8400-e29b-41d4-a716-446655440202	8-923-666-13-13	2025-08-05 17:27:00+03	019881d5-3642-7b12-a470-646d2ad87c6f
550e8400-e29b-41d4-a716-446655440203	4-444-444	2025-08-05 17:27:00+03	019881d5-3643-7408-8a5c-457291bea525
\.


--
-- TOC entry 4656 (class 2606 OID 400666)
-- Name: activity activity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_pkey PRIMARY KEY (id);


--
-- TOC entry 4654 (class 2606 OID 400659)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 4658 (class 2606 OID 400678)
-- Name: building building_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_pkey PRIMARY KEY (id);


--
-- TOC entry 4662 (class 2606 OID 400695)
-- Name: organization_activity organization_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_activity
    ADD CONSTRAINT organization_activity_pkey PRIMARY KEY (id);


--
-- TOC entry 4664 (class 2606 OID 400712)
-- Name: organization_phone organization_phone_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_phone
    ADD CONSTRAINT organization_phone_pkey PRIMARY KEY (id);


--
-- TOC entry 4660 (class 2606 OID 400685)
-- Name: organization organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id);


--
-- TOC entry 4665 (class 2606 OID 400667)
-- Name: activity activity_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.activity(id) ON DELETE CASCADE;


--
-- TOC entry 4667 (class 2606 OID 400696)
-- Name: organization_activity organization_activity_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_activity
    ADD CONSTRAINT organization_activity_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activity(id) ON DELETE RESTRICT;


--
-- TOC entry 4668 (class 2606 OID 400701)
-- Name: organization_activity organization_activity_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_activity
    ADD CONSTRAINT organization_activity_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id) ON DELETE CASCADE;


--
-- TOC entry 4666 (class 2606 OID 400686)
-- Name: organization organization_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.building(id) ON DELETE RESTRICT;


--
-- TOC entry 4669 (class 2606 OID 400713)
-- Name: organization_phone organization_phone_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_phone
    ADD CONSTRAINT organization_phone_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id) ON DELETE CASCADE;


-- Completed on 2025-08-07 03:02:34

--
-- PostgreSQL database dump complete
--

