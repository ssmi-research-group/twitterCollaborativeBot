# WhoKnowsBot

## Overview do projeto

WhoKnowsBot é um robô social. Ele foi desenvolvido como um estudo de caso sobre desenvolvimento de componentes de software associados a computação por humanos (human computation). O estudo é parte do projeto PIBIC-CNPq coordenado pelo prof. Lesandro Ponciano e conduzido pelo aluno bolsista Arthur Vinicius Soares, no curso Bacharelado em Sistemas de Informação da Pontifícia Universidade Católica de Minas Gerais (PUC Minas). O projeto foi executado entre Agosto de 2017 e Julho de 2018.

A partir de Agosto 2019, o WhoKnowsBot foi incorporado no projeto PIBIC-CNPq "O Requisito de Explicabilidade em Robôs Sociais que Implementam Computação por Humanos", também coordenado pelo prof. Lesandro Ponciano e conduzido pelo aluno bolsista Lucas Rotsen Pereira, no curso Bacharelado em Engenharia de Software da mesma instituição (PUC Minas).

De forma geral, o robô possui três funcionalidades principais que podem ser acionadas pelo usuário: atribuição, agregação e contagem de termos. Pela funcionalidade de atribuição (escalonamento), o usuário informa ao robô um tópico e o robô responde ao usuário quem (entre as pessoas que seguem o usuário no twitter) mais fala sobre aquele tópico no twitter. Pela funcionalidade de agregação, o usuário informa ao robô um tópico e o robô responde ao usuário quantas (entre as pessoas que o usuário segue no twitter) falaram sobre aquele tópico no twitter. Pela contagem de termos o robô enumera os termos mais frequentes na timeline do usuário e o responde com uma nuvem de palavras.

Há uma instância do robô ativa em https://twitter.com/whoknowsbot. Informações sobre como conversar com o robô e explicações sobre as respostas dele estão em https://drive.google.com/file/d/1jhFCTByFLM2uOGsqa_BUB0BR9FarKnlV/view.

Abaixo estão mais informações sobre a implementação do robô.

## Configuração inicial

As configurações do robô são acessadas através da pasta _configurarion_ localizada na raiz do projeto.

No arquivo _twitter_connection.py_ é necessário atribuir valores às variáveis:

    - consumerKey
    - consumerSecret
    - accessToken
    - accessTokenSecret

Essas informações estão disponíveis na [página do desenvolvedor](https://apps.twitter.com) do Twitter:

    consumerKey = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
    consumerSecret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    accessToken = '0000000000-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    accessTokenSecret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

No arquivo _bot_config.py_ existem três parâmetros que influenciam no comportamento do robô:

    - verbose
    - amount_of_terms_to_retrieve
    - should_count_mentions

O parâmetro _verbose_ especifica se o robô deve imprimir no console os passos de sua execução. Por padrão este valor é **True**.

O parâmetro _amount_of_terms_to_retrieve_ define a quantidade de termos que serão retornados pelo método _most_used_terms_. Por padrão este valor é **10**.

O parâmetro _should_count_mentions_ especifica se o método _most_used_terms_ deve contar menções. **Exemplo**: No tweet "@dan_abramov I love react" os termos "love" e "react" seriam contados uma vez cada e os termos "I" e "@dan_abramov" seriam ignorados. Caso `should_count_mentions = True`, o termo "@dan_abramov" também seria contado. Por padrão este valor é **False**.

## Executando o Robô

_Este projeto foi testado no sistema operacional Ubuntu 18.04 com Python 3.6.8._

Para executar o robô é necessário instalar as dependências do projeto. No Ubuntu 18.04 a instalação pode ser feita executando o script _whoknowsbot-config.sh_ na pasta raiz do projeto:

     $ chmod +x whoknowsbot-config.sh && ./whoknowsbot-config.sh

Ao executar o script acima, as seguintes dependências serão instaladas:

    1. python3-pip
    2. setuptools
    3. python-twitter
    4. nltk
    5. wordcloud
    6. backoff
    7. matplotlib

No Ubuntu 18.04 a instalação manual pode ser feita executando o comando:

    $ sudo python3 -m pip install [dependência]

Para acessar as funcionalidades do robô sem a interação pelo Twitter, forneça o username do usuário que será analisado e o termo desejado:

     $ python main.py [screen_name] [termo]

Executando `python main.py dan_abramov react` as funcionalidades providas pelo robô serão executadas para o usuário Dan Abramov em relação ao termo 'react'. As saídas dos algoritmos serão salvas no arquivo 'result.txt' na pasta raiz do projeto.

_O robô do Twitter está em um loop infinito, quando necessário deve-se interrompê-lo manualmente._

## Ativação do script

Com o script executando, sempre que novas menções são direcionadas à conta do Twitter associado às variáveis definidas acima, inicia-se a análise de cada menção individualmente.

_Por conta de limites da API, a verificação de novas menções ocorrem de 1 em 1 minuto._

Quando não há novas menções o script hiberna por 1 minutos, e verifica novamente novas menções.

## Análise das menções

A função _listener()_ é a primeira função a ser chamada no script. Ela é responsável pela coleta de novas menções, e determinar qual a próxima função a ser chamada de acordo com o conteúdo da menção. Para cada menção que é coletada, a string com seu conteúdo é quebrada, e verifica-se se o termo que o usuário utilizou. As opções padrões são limitadas ao uso dos termos QUEMSABE, QUANTOSSABEM e SOBREOQUESABEM.

A forma como será decidido qual fluxo seguir pode ser personalizada conforme o uso que será dado ao script.

## Quantos sabem

Essa análise foca em descobrir quantos amigos falaram sobre um termo.

É feita a coleta das publicações de quem o mencionador segue (amigos), que foram criadas até 7 dias precedentes ao início da análise e que possuem em seu conteúdo um termo especificado na menção. A função _how_many_knows(self, mention)_ busca quais amigos utilizaram o termo em seus tweets e faz uma contagem desses amigos.

Veja abaixo o diagrama de sequência que representa essa análise:
![alt text](https://preview.ibb.co/mvy4So/image1.jpg "Diagrama de Sequência - Quantos sabem")

## Quem sabe

Essa análise foca em descobrir quem é o melhor seguidor para responder algo sobre um termo.

É feita a coleta das publicações de quem segue o mencionador (seguidores), que foram criadas até 7 dias precedentes ao início da análise e que possuem em seu conteúdo um termo especificado na menção. A da função _who_knows(self, mention)_ busca quais seguidores utilizaram o termo em seus tweets. Em seguida, busca-se a publicação mais antiga, que servirá de referência para selecionar o melhor seguidor.

Para cada seguidor é feito o cálculo de uma pontuação que representa sua aptidão para responder alguma pergunta sobre o termo especificado. Sua pontuação aumenta a cada publicação que possui o termo, conforme a fórmula abaixo:

![alt text](https://preview.ibb.co/cRjaHo/image4.png "Fórmula - Quem sabe")

    - <b>Pw</b> é pontuação do seguidor w;
    - <b>a</b> é publicação do seguidor w;
    - <b>Tw,a</b> é o timestamp da publicação a;
    - <b>T*</b> é o timestamp da publicação mais antiga
    - <b>now</b> é timestamp no momento da decisão de escalonamento (horário do sistema).

Ao final é retornado o seguidor com a melhor pontuação.
Veja abaixo o diagrama de sequência que representa essa análise:

![alt text](https://preview.ibb.co/dGL17o/image3.jpg "Diagrama de Sequência - Quem sabe")

## Sobre o que sabem

Essa análise foca em descobrir a frequência dos termos que aparecem na timeline do usuário.

É feita a coleta das publicações de quem o mencionador segue (amigos), que foram criadas até 7 dias precedentes ao início da análise e que possuem em seu conteúdo um termo especificado na menção. A função _most_used_terms(api, user_id, user_name)_ recupera os termos usados nas publicações e faz uma contagem destes.

A contagem de termos é feita utilizando a biblioteca [nltk](https://www.nltk.org). Textos podem conter palavras que não são relevantes na contagem (stop words) como: ele, ela, aquilo, isso. Estas palavras são removidas utilizando uma lista de palavras proveniente da biblioteca em conjunto com uma lista customizada presente no arquivo `resources/text/custom_stopwords.py`. Por consequência desta dependência de listas de stop words a funcionalidade de contagem de termos suporta apenas as linguagens inglês e português.

Veja abaixo o diagrama de sequência que representa essa análise:

![alt text](https://i.ibb.co/NS6k1TB/Counting-algorithm.jpg "Diagrama de Sequência - Termos mais usados")

## Respostas

Após a análise de cada menção, o mencionador é respondido, conforme o resultado opções dispiníveis no arquivo _mentions_replies.py_, podendo ser:

Para análise do tipo QUANTOSSABEM:

    - reply_mention_how_many(api, data, mention)

Para análise do tipo QUEMSABE:

    - reply_mention_who_know(api, data, mention)

Para análise do tipo SOBREOQUESABEM:

    - reply_mention_most_used_terms(api, data, mention)

Ou para menções em formato inválido:

    - reply_invalid_tweet(api, mention)
