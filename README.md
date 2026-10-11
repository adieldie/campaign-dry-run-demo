# Pré-validação de campanhas — demonstração offline

**Estágio: experimental / em teste. Demonstração parcial sanitizada, não pronta para produção.**

## Objetivo
Um recorte de motor de pré-validação com relatório dry-run.

## Recursos
Campos obrigatórios, regras ilustrativas de conteúdo, resultados PASS/REVIEW_REQUIRED/BLOCK e confirmação separada.

## Instalação
Python 3.10+; sem dependências externas. Baixe somente os arquivos desta demonstração para uma pasta local.

## Uso e testes
```sh
python demo.py
python -m unittest -v
```

## Estágio e limites
Demonstração parcial de lógica extraída e adaptada, não uma cópia integral do sistema original. Fixtures e entradas são inteiramente fictícias.

Não cria campanhas, não se conecta a contas e não implementa um servidor MCP. As regras são exemplos técnicos e não representam validação jurídica, regulatória ou política atual de qualquer plataforma. Um PASS não garante elegibilidade. can_proceed permanece falso, mesmo quando a simulação passa.

## Dados e segurança
Não inclui configurações operacionais, contas, histórico de conversas, bancos de dados, capturas de rede, segredos ou endpoints de produção. Nenhum envio externo ocorre.

## Licença
Nenhuma licença de redistribuição é atribuída automaticamente. A definição de licença depende de revisão dos direitos aplicáveis antes da publicação.
