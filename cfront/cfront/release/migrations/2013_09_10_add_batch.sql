--
-- Name: batch; Type: TABLE; Schema: public; Owner: ben; Tablespace: 
--

CREATE TABLE batch (
    id bigint NOT NULL,
    date_submitted timestamp without time zone NOT NULL,
    genome integer NOT NULL,
    key character varying NOT NULL,
    original_filename character varying,
    name character varying,
    email character varying,
    date_completed timestamp without time zone,
    failed boolean NOT NULL,
    date_failed timestamp without time zone,
    error_traceback character varying,
    error_message character varying,
    email_complete boolean NOT NULL,
    has_emailed boolean NOT NULL
);

ALTER TABLE public.batch OWNER TO ben;

--
-- Name: addbatchid bigint key to job
--

ALTER TABLE job ADD COLUMN batchid bigint;

--
-- Name: batch_id_seq; Type: SEQUENCE; Schema: public; Owner: ben
--

CREATE SEQUENCE batch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.batch_id_seq OWNER TO ben;


--
-- Name: batch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ben
--

ALTER SEQUENCE batch_id_seq OWNED BY batch.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ben
--

ALTER TABLE ONLY batch ALTER COLUMN id SET DEFAULT nextval('batch_id_seq'::regclass);

--
-- Name: batch_pkey; Type: CONSTRAINT; Schema: public; Owner: ben; Tablespace: 
--

ALTER TABLE ONLY batch
    ADD CONSTRAINT batch_pkey PRIMARY KEY (id);

--
-- Name: ix_batch_key; Type: INDEX; Schema: public; Owner: ben; Tablespace: 
--

CREATE UNIQUE INDEX ix_batch_key ON batch USING btree (key);

--
-- Name: job_batchid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ben
--

ALTER TABLE ONLY job
    ADD CONSTRAINT job_batchid_fkey FOREIGN KEY (batchid) REFERENCES batch(id);

