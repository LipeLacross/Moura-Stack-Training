function mostrarnumerosprimos(array: number[]): number[] {
    let primos: number[] = []; 
    
    for (let i = 0; i < array.length; i++) {
        let esPrimo = true;
        if (array[i] < 2) {
            esPrimo = false;
        } else {
            for (let j = 2; j <= Math.sqrt(array[i]); j++) {
                if (array[i] % j === 0) {
                    esPrimo = false;
                    break;
                }
            }
        }
        if (esPrimo) {
            primos.push(array[i]);
        }
    }
    return primos;
}

const meuarray: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log(mostrarnumerosprimos(meuarray));


console.log("Alô, terminal! Estou funcionando!");