# Sistema de Gerenciamento de Serviços de Metrô

Este projeto tem como objetivo implementar um banco de dados para um sistema de gerenciamento de serviços de metrô. O sistema será responsável por armazenar e gerenciar informações detalhadas sobre as linhas de metrô, trajetos, estações, itinerários, motoristas, usuários, empresas, cidades e incidentes. 

## Objetivo

O principal objetivo deste sistema é fornecer um banco de dados eficiente para facilitar a consulta e o gerenciamento das operações diárias do metrô. O sistema permitirá que:

- Usuários consultem informações como:
  - Linhas de metrô disponíveis
  - Itinerários de cada linha
  - Trajetos e as estações correspondentes
  - Horários de operação

- Administradores realizem operações como:
  - Atualização de trajetos
  - Gerenciamento de motoristas (vinculação de motoristas às linhas, alteração ou remoção)
  - Exclusão de linhas ou trajetos

- Dentre outras operações.

## Funcionalidades

### Usuários Comuns
- Consulta de linhas, estações e itinerários
- Visualização dos horários de operação das linhas

### Administradores
- Atualização de trajetos de linhas
- Gerenciamento de motoristas (inclusão, alteração, remoção)
- Exclusão de linhas e trajetos
- Gerenciamento de empresas e cidades relacionadas ao sistema

## Estrutura de Dados

O sistema armazenará diversas informações, incluindo:

- **Linhas de metrô**: Dados sobre cada linha e seus itinerários
- **Trajetos**: Caminhos que os metrôs percorrem em uma linha específica
- **Estações**: Localizações das paradas ao longo de um trajeto
- **Motoristas**: Informações detalhadas dos motoristas, como foto 3x4, contato e linha associada
- **Empresas e Cidades**: Relacionamentos entre as cidades atendidas e as empresas que gerenciam as operações
- **Incidentes**: Registro de incidentes ocorridos no sistema, se necessário

O sistema foi desenvolvido para ser **escalável**, permitindo a adição de novas estações, linhas, motoristas e empresas, garantindo a **integridade e consistência dos dados** armazenados.

## Tecnologias Utilizadas

Este projeto é composto por três camadas principais:

1. **Persistência de Dados**: 
   - Utiliza **PostgreSQL** para o gerenciamento e armazenamento de dados.
   
2. **Camada de Negócios**:
   - Implementada em **Python**, onde toda a lógica de negócios do sistema é processada.
   
3. **Camada de Apresentação**:
   - Desenvolvida com **Flask**, fornecendo uma interface para interação com o sistema. Usuários e administradores podem acessar as funcionalidades de maneira simples e intuitiva.

## Desenvolvedores
Este projeto foi desenvolvido por:
  - Arthur  -> Artdelpi
  - Geilson -> Geilsondss
  - Victor  -> VictorFontesCavalcante
  - Wesley  -> ShadowmereSmith
