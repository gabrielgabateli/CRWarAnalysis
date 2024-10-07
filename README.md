# CRWarAnalysis

Esse é um projeto que automatiza o processo de análise da guerra do clash royale controlado por parâmetros globais. É dividido em duas análises:  
- Análise de Guerra
	- Menos de 400 pontos -> EXPULSO;
	- Entre 400 e 1800 -> BLACKLIST;

- Análise de Promoção
	- Média dos top 5 em duas guerras seguidas;
	- Quem tiver mais de 2700 -> PROMOÇÃO ANCIÃO;

## TODO

- [x] (GUERRA) Verificar se o player está na primeira blacklist ou na segunda blacklist seguida
- [ ] (GUERRA) Montar uma tabela de decks usados por player com o critério (8 DECKS USADOS OU MENOS)
- [X] (GUERRA) Verificar se o player ainda está no clã, se não estiver não precisa mostrar o nome dele na lista de expulsos  
- [X] (GUERRA) Adicionar variáveis de pontuação mínima, intermediária etc no arquivo variables.py para controlar melhor  
- [ ] (GUERRA) Integrar banco de dados pra ter histórico de análise e de blacklist  
- [X] (GUERRA) Subir o projeto em uma VM ou cron no Termux pra rodar automaticamente  
- [X] (GUERRA) Formatar o e-mail como HTML pra colocar os dados em uma tabela e facilitar a visualização  
- [ ] (PROMOÇÃO) Iniciar o projeto 
