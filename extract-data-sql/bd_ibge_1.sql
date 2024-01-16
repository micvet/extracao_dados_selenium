create database geo_ibge_data;


create sequence regiao_id_seq START 1;
create table regiao (
    regiao_id numeric (2) default nextval('regiao_id_seq') PRIMARY key,
    regiao_nome varchar(15) not null
);


create sequence uf_id_seq START 1;
create table uf (
    uf_id numeric(2) default nextval('uf_id_seq') PRIMARY key,
    uf_nome varchar(30) not null,
    uf_regiao_id numeric (2),
    foreign key (uf_regiao_id) references regiao(regiao_id)
    
);


create sequence cidade_id_seq START 1;
create table dados_cidade (
    cidade_id numeric (10) default nextval('cidade_id_seq') PRIMARY key,
    uf_id numeric (2),
    cidade_nome varchar(255) not null,
    prefeito_nome varchar(255),
    territorio numeric(20,3),
    foreign key (uf_id) references uf(uf_id)
    
);

create sequence populacao_id_seq START 1;
create table dados_populacao (
    populacao_id numeric (10) default nextval('populacao_id_seq') PRIMARY key,
    cidade_id numeric (10),
    populacao_valor numeric (20),
    densidade_valor numeric (20,2),
    foreign key (cidade_id) references dados_cidade(cidade_id)
);

create sequence bem_estar_id_seq START 1;
create table indices_bem_estar (
    indices_id numeric (10) default nextval('bem_estar_id_seq') PRIMARY key,
    cidade_id numeric (10),
    mortalidade_infantil_valor numeric (10,2),
    idhm_valor numeric(5,3),
    escolarizacao_valor numeric (20,2),
    foreign key (cidade_id) references dados_cidade(cidade_id)
);

create sequence financas_id_seq START 1;
create table dados_financas (
    financas_id numeric (10) default nextval('financas_id_seq') PRIMARY key,
    cidade_id numeric (10),
    receitas_valor numeric(20),
    despesas_valor numeric(20),
    pib_per_capta_valor numeric(20),
    foreign key (cidade_id) references dados_cidade(cidade_id)
);




