# MerkleDAGs
Implementations of various merkle-based structures in Python 

## Merkle Trees
A Merkle-Tree is a binary tree constructed from a list of data elements (the leaves of the tree). Each leaf is labelled 
with a cryptographic hash of its contents with all internal nodes labelled with the cryptographic hash of the 
cryptographic hashes of its children.

Doing so guarantees that if two nodes' hashes match they represent the same Merkle Tree (since this is a recursively 
defined data-structure).

Thus one can compare a vast amount of content by comparing only root-hashes. 

Our implementation makes the following restriction:

  - The initial data must be in a Python List.  

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