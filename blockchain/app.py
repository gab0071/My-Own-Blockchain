# Importación de las librerías
import datetime
import hashlib
import json
from flask  import Flask, jsonify
from flask_ngrok import run_with_ngrok

"""  
Creación de una clase Blockchain que contenga todos los métodos esenciales, como son los siguientes:

* Creación de un nuevo bloque
* Obtención del hash de un bloque
* Protocolo de concenso Proof of Work (PoW)
* Generación del hash de un bloque
* Verificación de la validez de la Blockchain

"""
class Blockchain:
    
  def __init__(self):
    """ Constructor de la clase Blockchain. """

    self.chain = []
    self.create_block(proof = 1, previous_hash = '0')
      
  
  def create_block(self, proof, previous_hash):
    """ Creación de un nuevo bloque. 

      Arguments:
        - proof: Nounce del bloque actual. (proof != hash)
        - previous_hash: Hash del bloque previo.

      Returns: 
        - block: Nuevo bloque creado. 
      """

    block = { 'index'         : len(self.chain)+1,
              'timestamp'     : str(datetime.datetime.now()),
              'proof'         : proof,
              'previous_hash' : previous_hash}
    self.chain.append(block)
    return block

  def get_previous_block(self):
    """ Obtención del bloque previo de la Blockchain .
    
      Returns:
        - Obtención del último bloque de la Blockchain. """

    return self.chain[-1]
  
  def proof_of_work(self, previous_proof):
    """ Protocolo de concenso Proof of Work (PoW).
    
      Arguments:
        - previous_proof: Nounce del bloque previo.

      Returns:
        - new_proof: Devolución del nuevo nounce obtenido con PoW. """

    new_proof = 1
    check_proof = False
    while check_proof is False:
        hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:2] == '00':
            check_proof = True
        else: 
            new_proof += 1
    return new_proof
  
  def hash(self, block):
    """ Cálculo del hash de un bloque.
    
    Arguments:
        - block: Identifica a un bloque de la Blockchain.
    
    Returns:
        - hash_block: Devuelve el hash del bloque """

    encoded_block = json.dumps(block, sort_keys = True).encode()
    hash_block = hashlib.sha256(encoded_block).hexdigest()
    return hash_block
  
  def is_chain_valid(self, chain):
    """ Determina si la Blockchain es válida. 
    
    Arguments:
        - chain: Cadena de bloques que contiene toda la 
                  información de las transacciones.
    
    Returns:
        - True/False: Devuelve un booleano en función de la validez de la 
                      Blockchain. (True = Válida, False = Inválida) """

    previous_block = chain[0]
    block_index = 1
    while block_index < len(chain):
        block = chain[block_index]
        if block['previous_hash'] != self.hash(previous_block):
            return False
        previous_proof = previous_block['proof']
        proof = block['proof']
        hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:2] != '00':
            return False
        previous_block = block
        block_index += 1
    return True

######

"""
Llamadas a realizar vía REST API:

* Minación de bloques: mine_block()
* Obtención de la Blockchain: get_chain()
* Comprobar estado de la Blockchain: is_valid()

"""

# Crear una aplicación web
# Ejecución de la app con Notebook
app = Flask(__name__)
run_with_ngrok(app)  

# Si se obtiene un error 500, actualizar flask y ejecutar la siguiente línea
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creación de la Blockchain
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
  """ Minado de un nuevo bloque """

  previous_block  = blockchain.get_previous_block()
  previous_proof  = previous_block['proof']
  proof           = blockchain.proof_of_work(previous_proof)
  previous_hash   = blockchain.hash(previous_block)
  block           = blockchain.create_block(proof, previous_hash)
  response = {'message'       : '¡felicidades crack, has minado un nuevo bloque 🎉!', 
              'index'         : block['index'],
              'timestamp'     : block['timestamp'],
              'proof'         : block['proof'],
              'previous_hash' : block['previous_hash']}
  return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
  """ Obtención de la Blockchain """
  response = {'chain'   : blockchain.chain, 
              'length'  : len(blockchain.chain)}
  return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
  """ Comprobación si la Blockchain es válida """

  is_valid = blockchain.is_chain_valid(blockchain.chain)
  if is_valid:
      response = {'message' : '¡La cadena de bloques es válida!'}
  else:
      response = {'message' : '¡La cadena de bloques NO es válida!'}
  return jsonify(response), 200



    


