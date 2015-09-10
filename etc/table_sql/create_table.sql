
--固定资产表--
CREATE TABLE tb_asset_info
(
  asset_id character varying(20) NOT NULL,
  device_state_id integer,
  user_name character varying(30) NOT NULL,
  up_time timestamp without time zone,
  create_time timestamp without time zone NOT NULL DEFAULT now(),
  update_time timestamp without time zone,
  remark character varying(100),
  in_out_reason_id integer NOT NULL,
  sn character varying(30),
  model_id integer,
  store_place_id integer,
  type_info hstore,
  asset_type_id integer,
  store_state_id integer
);

--电话号码表
CREATE TABLE tb_asset_phone_info
(
  id serial NOT NULL,
  asset_type_id integer,
  store_place_id integer,
  store_state_id integer,
  device_state_id integer,
  in_out_reason_id integer,
  phone_no character varying(20),
  user_name character varying(20),
  up_time timestamp without time zone,
  create_time timestamp without time zone,
  update_time timestamp without time zone,
  remark character varying(30)
);

--耗材类表--
CREATE TABLE tb_asset_consume_info
(
  id serial NOT NULL,
  asset_type_id integer,
  store_place_id integer,
  store_state_id integer,
  device_state_id integer,
  in_out_reason_id integer,
  model_id integer,
  in_num integer,
  out_num integer,
  user_name character varying(20),
  up_time timestamp without time zone,
  create_time timestamp without time zone,
  update_time timestamp without time zone,
  remark character varying(30)
);

--操作日志记录表--
CREATE TABLE tb_operation_info
(
  id serial NOT NULL,
  asset_id character varying(20) NOT NULL,
  oper_time timestamp without time zone,
  oper_type character varying(10),
  operator character varying(30) NOT NULL,
  text character varying(100) NOT NULL,
  before_field hstore,
  after_field hstore
);

--品牌表--
CREATE TABLE mp_provider
(
  id serial NOT NULL,
  name character varying(20),
  ch_name character varying(20),
  asset_type_id integer,
  CONSTRAINT tb_provider_pkey PRIMARY KEY (id)
);

--型号表--
CREATE TABLE mp_model
(
  id serial NOT NULL,
  provider_id integer,
  name character varying(20),
  CONSTRAINT tb_model_pkey PRIMARY KEY (id)
);

--资产类别表
CREATE TABLE dt_asset_type
(
  id serial NOT NULL,
  ch_name character varying(15) NOT NULL,
  asset_path ltree,
  CONSTRAINT id PRIMARY KEY (id)
);

--资产状态表--
CREATE TABLE dt_device_state
(
  id serial NOT NULL,
  ch_name character varying(15) NOT NULL,
  CONSTRAINT device_id PRIMARY KEY (id)
);

--库存状态表--
CREATE TABLE dt_store_state
(
  id serial NOT NULL,
  ch_name character varying(20),
  CONSTRAINT dt_store_state_pkey PRIMARY KEY (id)
);

--库房地点表--
CREATE TABLE dt_store_place
(
  id serial NOT NULL,
  ch_name character varying(20),
  admin_name character varying(30),
  CONSTRAINT dt_store_place_pkey PRIMARY KEY (id)
);

--出入库原因表--
CREATE TABLE dt_in_out_reason
(
  id serial NOT NULL,
  in_or_out character varying(20),
  ch_name character varying(20),
  CONSTRAINT dt_in_out_reason_pkey PRIMARY KEY (id)
);