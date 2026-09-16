# కందము · kandamu

```mermaid
flowchart LR
  subgraph odd["slot odd"]
    direction LR
    odd_start(( ))
    odd_G1["G1<br/>భ UII  /  స IIU<br/>నల IIII  /  గా UU"]
    odd_start --> odd_G1
    odd_G2["G2<br/>భ UII  /  జ IUI<br/>స IIU  /  నల IIII<br/>గా UU"]
    odd_G1 --> odd_G2
    odd_G3["G3<br/>భ UII  /  స IIU<br/>నల IIII  /  గా UU"]
    odd_G2 --> odd_G3
    odd_end((( )))
    odd_G3 --> odd_end
  end
  subgraph even["slot even"]
    direction LR
    even_start(( ))
    even_G1["G1<br/>భ UII  /  జ IUI<br/>స IIU  /  నల IIII<br/>గా UU"]
    even_start --> even_G1
    even_G2["G2<br/>భ UII  /  స IIU<br/>నల IIII  /  గా UU"]
    even_G1 --> even_G2
    even_G3["G3<br/>జ IUI  /  నల IIII"]
    even_G2 --> even_G3
    even_G4["G4<br/>భ UII  /  స IIU<br/>నల IIII  /  గా UU<br/>◆ యతి (gana start)"]
    even_G3 --> even_G4
    even_G5["G5<br/>స IIU  /  గా UU"]
    even_G4 --> even_G5
    even_end((( )))
    even_G5 --> even_end
  end
  classDef yati fill:#ffe082,stroke:#f9a825;
  class even_G4 yati;
```
