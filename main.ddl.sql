-- StagingAccount --

CREATE TABLE IF NOT EXISTS public."SLVK_stg_accounts" (
	account VARCHAR NOT NULL,
	valid_to TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	client VARCHAR NOT NULL,
	PRIMARY KEY (account)
)


-- DimAccount --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_accounts" (
	account VARCHAR NOT NULL,
	valid_to TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	client VARCHAR NOT NULL,
	create_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	update_dt TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (account),
	UNIQUE (account),
	FOREIGN KEY(client) REFERENCES public."SLVK_dwh_dim_clients" (client_id)
)


-- DimAccountHist --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_accounts_hist" (
	account VARCHAR NOT NULL,
	valid_to TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	client VARCHAR NOT NULL,
	effective_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	effective_to TIMESTAMP WITHOUT TIME ZONE,
	deleted_flg BOOLEAN NOT NULL,
	PRIMARY KEY (account, effective_from)
)


-- StagingPassportBlacklist --

CREATE TABLE IF NOT EXISTS public."SLVK_stg_blacklist" (
	date DATE NOT NULL,
	passport VARCHAR(11) NOT NULL,
	PRIMARY KEY (date, passport)
)


-- FactPassportBlacklist --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_fact_passport_blacklist" (
	id SERIAL NOT NULL,
	date DATE NOT NULL,
	passport VARCHAR(11) NOT NULL,
	PRIMARY KEY (id, date, passport)
)


-- StagingCard --

CREATE TABLE IF NOT EXISTS public."SLVK_stg_cards" (
	card_num VARCHAR(19) NOT NULL,
	account VARCHAR(22) NOT NULL,
	PRIMARY KEY (card_num)
)


-- DimCard --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_cards" (
	card_num VARCHAR(19) NOT NULL,
	account VARCHAR(22) NOT NULL,
	create_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	update_dt TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (card_num),
	UNIQUE (card_num),
	FOREIGN KEY(account) REFERENCES public."SLVK_dwh_dim_accounts" (account)
)


-- DimCardHist --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_cards_hist" (
	card_num VARCHAR(19) NOT NULL,
	account VARCHAR(22) NOT NULL,
	effective_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	effective_to TIMESTAMP WITHOUT TIME ZONE,
	deleted_flg BOOLEAN NOT NULL,
	PRIMARY KEY (card_num, effective_from)
)


-- StagingClient --

CREATE TABLE IF NOT EXISTS public."SLVK_stg_clients" (
	client_id VARCHAR NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	first_name VARCHAR(255) NOT NULL,
	patronymic VARCHAR(255),
	date_of_birth TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	passport_num VARCHAR(20) NOT NULL,
	passport_valid_to TIMESTAMP WITHOUT TIME ZONE,
	phone VARCHAR(20) NOT NULL,
	PRIMARY KEY (client_id)
)


-- DimClient --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_clients" (
	client_id VARCHAR NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	first_name VARCHAR(255) NOT NULL,
	patronymic VARCHAR(255),
	date_of_birth TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	passport_num VARCHAR(20) NOT NULL,
	passport_valid_to TIMESTAMP WITHOUT TIME ZONE,
	phone VARCHAR(20) NOT NULL,
	create_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	update_dt TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (client_id)
)


-- DimClientHist --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_clients_hist" (
	client_id VARCHAR NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	first_name VARCHAR(255) NOT NULL,
	patronymic VARCHAR(255),
	date_of_birth TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	passport_num VARCHAR(20) NOT NULL,
	passport_valid_to TIMESTAMP WITHOUT TIME ZONE,
	phone VARCHAR(20) NOT NULL,
	effective_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	effective_to TIMESTAMP WITHOUT TIME ZONE,
	deleted_flg BOOLEAN NOT NULL,
	PRIMARY KEY (client_id, effective_from)
)


-- FraudReport --

CREATE TABLE IF NOT EXISTS public."SLVK_rep_fraud" (
	id SERIAL NOT NULL,
	event_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	passport VARCHAR(20) NOT NULL,
	fio VARCHAR NOT NULL,
	phone VARCHAR(20),
	event_type VARCHAR NOT NULL,
	report_dt DATE NOT NULL,
	PRIMARY KEY (id)
)


-- StagingTerminal --

CREATE TABLE IF NOT EXISTS public."SLVK_stg_terminals" (
	id VARCHAR(10) NOT NULL,
	type VARCHAR(50) NOT NULL,
	city VARCHAR(100) NOT NULL,
	address VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
)


-- DimTerminal --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_terminals" (
	id VARCHAR(10) NOT NULL,
	type VARCHAR(50) NOT NULL,
	city VARCHAR(100) NOT NULL,
	address VARCHAR(255) NOT NULL,
	create_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	update_dt TIMESTAMP WITHOUT TIME ZONE,
	PRIMARY KEY (id)
)


-- DimTerminalHist --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_dim_terminals_hist" (
	id VARCHAR(10) NOT NULL,
	type VARCHAR(50) NOT NULL,
	city VARCHAR(100) NOT NULL,
	address VARCHAR(255) NOT NULL,
	effective_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	effective_to TIMESTAMP WITHOUT TIME ZONE,
	deleted_flg BOOLEAN NOT NULL,
	PRIMARY KEY (id, effective_from)
)


-- StagingTransaction --

CREATE TABLE IF NOT EXISTS public."SLVK_stg_transactions" (
	id VARCHAR NOT NULL,
	date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	amount FLOAT NOT NULL,
	card_num VARCHAR NOT NULL,
	oper_type VARCHAR NOT NULL,
	oper_result VARCHAR NOT NULL,
	terminal VARCHAR NOT NULL,
	PRIMARY KEY (id)
)


-- FactTransaction --

CREATE TABLE IF NOT EXISTS public."SLVK_dwh_fact_transactions" (
	id VARCHAR NOT NULL,
	date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	amount FLOAT NOT NULL,
	card_num VARCHAR NOT NULL,
	oper_type VARCHAR NOT NULL,
	oper_result VARCHAR NOT NULL,
	terminal VARCHAR NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(card_num) REFERENCES public."SLVK_dwh_dim_cards" (card_num),
	FOREIGN KEY(terminal) REFERENCES public."SLVK_dwh_dim_terminals" (id)
)
