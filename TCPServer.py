#Importa modulo de soquete
from socket import *    

#Cria um soquete do servidor TCP
#(AF_INET usado para protocolos IPv4)
#(SOCK_STREAM e usado para TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Atribui um numero de porta
serverPort = 9900

#Associa o numero de porta do servidor ao socket
serverSocket.bind(("", serverPort)) 

#O servidor "escuta" as requisicoes TCP do client. O parametro especifica o numero maximo de conexoes em fila(pelo menos 1).
serverSocket.listen(1)

# O servidor deve estar funcionando e "ouvindo" as conexoes de entrada
while 1:
	
	print 'The server is ready to receive'
	# Configura uma nova conexao do cliente
	connectionSocket, addr = serverSocket.accept()
	
	# Se ocorrer uma excecao durante a execucao da clausula try
        # o resto da clausula e ignorado
        # Se o tipo de excecao corresponder a palavra apos, exceto
        # a clausula except e executada
	try:
                # Recebe uma mensagem de solicitacao do cliente
		message =  connectionSocket.recv(1024)
		# Extrai o caminho do objeto solicitado da mensagem
                # O caminho e a segunda parte do cabecalho HTTP, identificado por [1]
		filename = message.split()[1]
		# Porque o caminho extraido da solicitacao HTTP inclui
                # Um caractere '\', lemos o caminho do segundo caractere
		f = open(filename[1:])
		# Armazena todo o conteudo do arquivo solicitado em um buffer temporario
		outputdata = f.read()
		# Envie a linha do cabecalho de resposta HTTP para o soquete de conexao
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")
 
		# Envie o conteudo do arquivo solicitado para o soquete de conexao
		for i in range(0, len(outputdata)):  
			connectionSocket.send(outputdata[i])
		connectionSocket.send("\r\n")
		
		# Fecha o soquete de conexao do cliente
		connectionSocket.close()

	except IOError:
                # Envia mensagem de resposta HTTP para o arquivo nao encontrado		
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
		# Fecha o soquete de conexao do cliente
		connectionSocket.close()

serverSocket.close()  

