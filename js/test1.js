async function funAsy() {
    const b = await new Promise((resolve, reject)=>{
         setTimeout(function(){
            resolve('time')
         }, 3000)
    }).then((res)=>{
        console.log('hello')
    })
    console.log(b)
 }

 async function funv() {
    await  funAsy()
    console.log('hellowww')
 }

 funv()