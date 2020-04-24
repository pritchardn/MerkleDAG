# MerkleDAGs
An implementations of a merkle-DAG in Python

## Merkle DAGs

A Merkle-DAG is very similar to a Merkle-Tree with two important changes:
  
  - It is a directed-acyclic-graph and not a tree
  - Every node can carry data, not just leaves

The resulting data-structure is constructed from leaf nodes since ancestors require the hash of their descendents 
in construction. 

Our implementation makes the following restriction:

  - Data must be primitive or a byte-array
   

## Installation on Windows
Installing the Cryptography library can be a pain on windows platforms
[help](https://stackoverflow.com/questions/45089805/pip-install-cryptography-in-windows)

## Dependencies
  - Networkx 

Our only dependency and is used to maintain the backbone DAG structure in our MerkleDAG 