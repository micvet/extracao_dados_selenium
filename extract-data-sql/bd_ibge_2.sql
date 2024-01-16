--Preparando as tabelas para receber os dados:

-- Primeiro inserir as regiões:

 insert into regiao (regiao_nome) values 
  	('NORTE'),
  	('CENTRO-OESTE'),
  	('NORDESTE'),
  	('SUDESTE'),
  	('SUL');
  
 -- Depois, inserir as UFs, já referenciadas com a região:
  
insert into uf (uf_nome, uf_regiao_id) values
    ('AC', 1),  
    ('AL', 3),  
    ('AM', 1),  
    ('AP', 1),  
    ('BA', 3), 
    ('CE', 3),  
    ('DF', 2),  
    ('ES', 4),  
    ('GO', 2),  
    ('MA', 3),  
    ('MG', 4),  
    ('MS', 2),  
    ('MT', 2),  
    ('PA', 1),  
    ('PB', 3),  
    ('PE', 3), 
    ('PI', 3),  
    ('PR', 5), 
    ('RJ', 4),
    ('RN', 3),
    ('RO', 1), 
    ('RR', 1),
    ('RS', 5),
    ('SC', 5),
    ('SE', 3),
    ('SP', 4), 
    ('TO', 1);  
   
   
--Verificando os dados inseridos:
select * from uf;
select * from regiao;
select uf_nome, regiao_nome from uf left join regiao on uf.uf_regiao_id = regiao.regiao_id ;
select * from dados_cidade ;

--Criando uma procedure para inserir os dados extraídos nas demais tabelas:

create function insere_dados(
    uf_param numeric (2),
    cidade_nome_param varchar (255),
    prefeito_nome_param varchar (255),
    territorio_param numeric (20),
    populacao_param numeric (20),
    densidade_param numeric (20),
    escolarizacao_param numeric (20),
    idhm_param numeric (20),
    mortalidade_infantil_param numeric (20),
    receitas_param numeric (20),
    despesas_param numeric (20),
    pib_param numeric (20)
)
returns void
language plpgsql
as $$
declare
    cidade_id_var numeric (10);
begin
    -- inserir cidade
    insert into dados_cidade (uf_id, cidade_nome, prefeito_nome, territorio)
    values (uf_param, cidade_nome_param, prefeito_nome_param, territorio_param)
    returning cidade_id into cidade_id_var;

    -- inserir população
    insert into dados_populacao (cidade_id, populacao_valor, densidade_valor)
    values (cidade_id_var, populacao_param, densidade_param);

    -- inserir índices de bem-estar
    insert into indices_bem_estar (cidade_id, mortalidade_infantil_valor, idhm_valor, escolarizacao_valor)
    values (cidade_id_var, mortalidade_infantil_param, idhm_param, escolarizacao_param);

    -- inserir dados financeiros
    insert into dados_financas (cidade_id, receitas_valor, despesas_valor, pib_per_capta_valor)
    values (cidade_id_var, receitas_param, despesas_param, pib_param);
end;
$$;


select insere_dados()

--verificando os dados inseridos por tabela
select * from dados_cidade ;
select * from dados_financas ;
select *from dados_populacao ;
select * from indices_bem_estar ;

select * from dados_financas
join dados_cidade on dados_cidade.cidade_id = dados_financas.cidade_id 
where cidade_nome = ('triunfo');

select cidade_nome, prefeito_nome, territorio, populacao_valor, densidade_valor, mortalidade_infantil_valor, idhm_valor, escolarizacao_valor, receitas_valor, despesas_valor, pib_per_capta_valor from dados_cidade
join dados_populacao on dados_cidade.cidade_id = dados_populacao.cidade_id
join indices_bem_estar on dados_cidade.cidade_id = indices_bem_estar.cidade_id
join dados_financas on dados_cidade.cidade_id = dados_financas.cidade_id;


