---
title: "Artigo Blog Webcoding"
date: 2025-10-23
---

## Desenvolvimento

Eu uso muito um aplicativo chamado One Deep Breath. Estou com um *streak* de três semanas, todos os dias tirando cinco ou dez minutos para fazer exercícios respiratórios com ele, quase sempre os mesmos: calm energy (5 segundos inspirandos - 2 expirando), calm (4 segundos inspirando - 6 expirando) e o box breathing.

Exercícos de respiração são, em uma lista muito enxuta de coisas que acredito de coração, uma verdadeira ferramenta de hackeamento da vida. Lembro até hoje quando meditei pela primeira vez e, consciente de minha respiração entendi que quem está ciente de sua respiração está ciente de si. E que quem está ciente de si está no controle. ^bb0c84

Por isso que gostei tanto do One Deep Breath, um app simples e funcional que oferece vários exercicios grátis e uma penca de outros pagos. Mas, também, ele é bem simples e fácil de replicar até certo ponto: ele oferece animações simples guiando a inspiração e a expiração (e as pausas quando isso é necessário). Basicamente um GIf com sons e capacidade de vibrar o celular. 

A construção do aplicativo Box Breathing mostra como a parceria entre inteligência artificial e criatividade humana pode criar soluções práticas e bonitas. Este processo colaborativo valoriza tanto o conhecimento técnico quanto o olhar humano em cada etapa. Vejamos os principais pontos dessa interação:

### 1. O papel humano no trabalho com IA

Durante o desenvolvimento, as decisões humanas foram essenciais para o sucesso do projeto. O assistente de IA gerou códigos rapidamente, mas foi o toque humano que trouxe melhorias importantes:

- **Simplificação visual:** percebi que ter um retângulo que expandia e contraía junto com o movimento do cursor era confuso, então optamos por um retângulo fixo com apenas o cursor se movendo.
- **Ajuste do ritmo:** notei e corrigi quando as mensagens na tela (Inspire, Segure, Expire, Segure) não estavam sincronizadas com os sinais sonoros.
- **Interface mais simples:** Após testes práticos, eliminei o botão de pausa e deixei apenas o botão "Parar", tornando o uso mais simples e fácil.

Verdade seja dita: ficou muito próximo da versão do app ODB, mas essa era a ideia, fazer um projeto de vibe coding simples e não muito criativo, mas que saísse do canvas e ganhasse o mundo.

### 2. Unindo técnica e sensibilidade

O sucesso da interface não vem apenas de códigos bem escritos (usei claude sonnet 3.7 em todas as interações, e também usei o deepseek no começo), mas também do entendimento sobre o que torna uma experiência agradável para o usuário. A capacidade de expressar ideias em linguagem comum e transformá-las em código funcional permite que pessoas sem formação técnica avançada possam criar produtos úteis e bonitos (ok, nem tão úteis e nem tão bonitos, mas que pelo menos é algo). Para isso, é importante ter noções básicas de programação e saber direcionar a IA. 

Até dá para ir sem nenhum preparo (conheci recentemente, mas não testei, o Loveable), mas imagino que não será uma experiencia tão enriquecedora como foi para mim, além de potencialmente negligenciar a agência humana no processo.

### 3. Intervenções humanas essenciais

Em cada fase do projeto, o olhar humano foi necessário para garantir qualidade e segurança:

- **Foco no essencial:** Saber quando parar de adicionar funções e manter o propósito central do aplicativo foi crucial para preservar sua "vibe".
- **Avaliação constante:** O feedback que eu dei ao chatbot - desde a escolha do layout até a sincronização dos elementos - garantiu que a aplicação funcionasse corretamente e de forma segura.

### 4. Responsabilidade pelo código gerado

Mesmo que os modelos de IA funcionem de forma complexa e às vezes pouco transparente, a responsabilidade final pelo que é criado é sempre do desenvolvedor. É importante estar ciente das limitações dos dados usados pela IA (muitos vindos de repositórios como o GitHub) e dos riscos potenciais, especialmente quando trabalhamos com informações sensíveis.

Por isso que Vibe coding pode ser um assunto espinhoso com algums devs, eles podem julgar irresponsável o uso - mas minha experiencia tem sido de apoio geral, de suscitar o uso e um chamado à criatividade - motivo pelo qual sempre elogio a comunidade dev - que me parece aberta e atenciosa.

### 5. Como melhorar os resultados da IA

Para obter melhores resultados da IA, algumas estratégias são úteis:

- **Fazer perguntas claras:** Pedir que a IA explique suas escolhas ajuda a identificar problemas e inconsistências.
- **Testar e ajustar:** Manter um ciclo contínuo de testes e melhorias garante que o produto final atenda às expectativas.
- **Pedir que se faça perguntas sobre o prompt:** isso eu aprendi em um forum do reddit - que ao fazer um prompt é bom pedir que o chatbot antes de responder faça perguntas elucidativas. Sempre funciona.

### 6. Liberdade criativa além dos padrões

Os grandes bancos de dados que alimentam as IAs podem impor certos padrões que limitam a criatividade. Usar ferramentas como o GitHub Copilot de forma mais livre permite experimentações que personalizam o código sem comprometer sua qualidade.

Acredito que temos espaço para o código como hobbie e o código sério - e que eles podem mesmo estar intrinsicamente ligados - quando o programador se desliga do metiè repetitivo de escrever códigos pode se libertar para focar em questões mais profundas do projeto.

### 7. Benefícios e cuidados éticos

A colaboração entre humanos e IA traz novas possibilidades:

- **Inclusão:** Pessoas que normalmente não conseguiriam programar agora podem criar soluções digitais.
- **Diversidade:** Mais vozes podem contribuir para o desenvolvimento tecnológico.

Porém, existem riscos a considerar:

- **Dependência:** Confiar demais nas sugestões da IA pode limitar o aprendizado técnico necessário para projetos importantes. Por isso é importante pedir que o chatbot consulte o humano em cada etapa do projeto.
- **Questões de autoria:** É preciso estabelecer limites claros sobre quem é responsável pelo produto final e como reconhecer contribuições originais. Uma abordagem possível é a de que, se a o LLM foi construído com dados protegidos então tudo o que usa LLM é por sua própria natureza de todos. 

---

Segue uma lista de 7 perguntas que podem orientar a conclusão do seu artigo, sintetizando as lições aprendidas e os desafios futuros na integração entre a agência humana e a assistência por IA:

1. De que maneira o projeto Box Breathing ilustra que, mesmo com a capacidade técnica da IA, a intervenção e o julgamento humano são insubstituíveis para garantir um produto final de qualidade?
    
2. Quais foram os principais aprendizados sobre a importância de iterar e refinar um produto digital por meio de feedback humano contínuo?
    
3. Como o equilíbrio entre a automação proporcionada pela IA e a sensibilidade crítica humana pode promover uma co-criação mais eficaz e segura?
    
4. Em que medida a democratização do desenvolvimento, possibilitada por ferramentas como o vibecoding, pode transformar a área da programação sem comprometer a responsabilidade e a segurança?
    
5. Quais estratégias emergentes podem ser adotadas para manter a originalidade e a autonomia criativa dos desenvolvedores diante dos padrões impostos pelos grandes datasets?
    
6. Como os desafios éticos – como transparência, autoria e dependência excessiva da IA – devem ser abordados para assegurar uma colaboração justa e sustentável entre humanos e máquinas?
    
7. De que forma a reflexão sobre inclusão e diversidade no uso das assistências por IA pode influenciar o futuro do desenvolvimento de software, ampliando as oportunidades para novos públicos e perspectivas?
    

Essas questões buscam sintetizar os pontos-chave abordados no desenvolvimento e direcionar uma reflexão crítica e abrangente sobre os desafios e oportunidades da colaboração humano-IA.