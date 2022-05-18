import deasync from "deasync";

export function syncPromise<TRes>(p: Promise<TRes>):TRes{
    var done = false;
    var res : TRes;
    p.then(x=>{
        res = x;
    }).catch(err=>{throw err;})
    .finally(()=>{
        done = true;
    });
    deasync.loopWhile(function(){return !done});
    return res;
}