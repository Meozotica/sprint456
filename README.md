# solução da Actividade das sprint 4,5 e 6.
#  crie uma página html que irá capturar uma frase qualquer inserida pelo usuário e transformará essa frase em um audio em mp3 via polly.
<h2>Descrição de funcionalidades do codigo</h2>
 <p>
 Utilizando boto3 para interagir com os serviços Amazon S3 e Amazon Polly. A solução da actividade é composta por três principais arquivos: generateaudio.py, handler.py e serverless.yml
 </p>


 <h2>tecnologias</h2>

 <h5>Serverless</h5>
 <h5>API Polly<h5>
 <h5>Boto3</h5>
 <h5>python<h5>
 <h5>tecnologias AWS: amazon polly, lambda, amazon s3 e API Gateway</h5>


<h3>generateaudio.py</h3>
<p>
Este arquivo contém a lógica para a conversão de texto para fala usando o serviço Amazon Polly. Ele também armazena o arquivo de áudio gerado no Amazon S3.A função principal ```generateMP3() recebe como parâmetros o texto a ser convertido em áudio e o nome do bucket do Amazon S3:
</p>
<p>
  1. Chama o serviço Amazon Polly usando o cliente boto3 para sintetizar o texto em um fluxo de áudio MP3;
	<br>
  2. Salva o fluxo de áudio em um arquivo local chamado "audio.mp3";
	<br>
  3. Verifica se o arquivo foi criado com êxito;
	<br>
  4. Carrega o arquivo MP3 para o bucket do Amazon S3.	
</p>

<h3>handler.py</h3>
<p>
Este arquivo contém as funções HTTP expostas pela API. Cada função é mapeada para uma rota específica e executa uma tarefa específica quando chamada:
</p>
<p>
<strong>createBucketMethod():</strong> Esta função verifica se um bucket do Amazon S3 com um nome específico existe. Se não existir, ela cria o bucket e retorna uma resposta com um código de status HTTP    200 e uma mensagem de sucesso. Se o bucket já existir, ela retorna uma mensagem informando isso. <br>
<strong>hello(event, context):</strong> Essa função é a rota raiz da API e retorna um código de status HTTP 200 e uma mensagem de sucesso quando chamada. <br>
<strong>health(event, context):</strong> Esta função é usada para testar se a aplicação está funcionando corretamente. Ela chama ```ceateBucketMethod() e retorna a resposta obtida.
</p>
<p>
 Com esta solução, podemos enviar uma frase para a rota "/v1/tts" e a função parte1().
</p>

<h3>Serverless.yml</h3>

<p>
 O arquivo "serverless.yml" é um arquivo de configuração usado pelo Framework Serverless para definir e implantar uma aplicação Serverless no AWS Lambda. Este arquivo define as funções, eventos, permissões e plugins usados na aplicação.

<p><strong>service:</strong> Define o nome do serviço, neste caso, "api-tts".</p> <br>
<p><strong>frameworkVersion:</strong>Especifica a versão do Serverless Framework que está sendo usada.</p>
<p><strong>functions: Aqui você definimos as funções lambda. Cada função tem um nome e um manipulador (o arquivo e a função dentro do arquivo que serão chamados quando a função lambda for acionada).</p>

<h3>Metodologia</h3>
<p>Para o desenvolvimento da aplção foi usada a metodologia ãgil, o grupo não fez a divisão de tarefas para produzir a solução, o grupo optou por desenvolver em conjunto parte por parte da apliçação com uma tela compartilhada e trocando ideias.
<br>
Foram realizadas dailys diárias que permitu cada elemento do grupo ter noção de qual é o rpogresso da solução e quais são as maiores dificuldades enfrentadas.</p>

<h3>Dificuldades enfrentadas</h3>
</p>
1. Conversão do arquivo em formato mp3 para ser arazenado no bucket tambem foi uma dificuldade e ate então conseguioms fazer apenas com o serverless offline.<br>
2. A outra dificuldade tem a ver com a criada uma lógica para que essa frase recebida seja um id unico.
</p> 
