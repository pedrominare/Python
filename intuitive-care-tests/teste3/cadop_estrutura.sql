-- Estrutura da tabela `dados`
--

CREATE TABLE `dados` (
  `data` date NOT NULL,
  `reg_ans` int(8) NOT NULL,
  `cd_conta_contabil` int(10) NOT NULL,
  `descricao` text NOT NULL,
  `vl_saldo_inicial` double NOT NULL,
  `vl_saldo_final` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estrutura da tabela `relatorio`
--

CREATE TABLE `relatorio` (
  `registroans` int(8) NOT NULL,
  `cnpj` varchar(20) NOT NULL,
  `razaosocial` text NOT NULL,
  `nomefantasia` text NOT NULL,
  `modalidade` text NOT NULL,
  `logradouro` text NOT NULL,
  `numero` text NOT NULL,
  `complemento` text NOT NULL,
  `bairro` text NOT NULL,
  `cidade` text NOT NULL,
  `uf` varchar(2) NOT NULL,
  `cep` varchar(10) NOT NULL,
  `ddd` int(3) NOT NULL,
  `telefone` varchar(10) NOT NULL,
  `fax` varchar(10) NOT NULL,
  `enderecoeletronico` text NOT NULL,
  `representante` text NOT NULL,
  `cargorepresentante` text NOT NULL,
  `dataregistroans` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Índices para tabela `dados`
--
ALTER TABLE `dados`
  ADD KEY `extrangeira` (`reg_ans`);

--
-- Índices para tabela `relatorio`
--
ALTER TABLE `relatorio`
  ADD PRIMARY KEY (`registroans`);

--
-- Limitadores para a tabela `dados`
--
ALTER TABLE `dados`
  ADD CONSTRAINT `extrangeira` FOREIGN KEY (`reg_ans`) REFERENCES `relatorio` (`registroans`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;
