// Staged checkout adapter. No live dashboard imports this file yet. The caller
// must initialize Paddle.js using the correct environment before using it.
export function createCheckoutUI({gateway,paddle}) {
  if(!gateway||typeof gateway.checkout!=='function'||!paddle||typeof paddle.Checkout?.open!=='function')throw Error('Checkout is not configured');
  let opening=false;
  async function open(plan,{autoRenew=false,discountCode=''}={}) {
    if(opening)return{opened:false,reason:'busy'};
    if(!['monthly','threeMonth','annual'].includes(plan)||typeof autoRenew!=='boolean'||typeof discountCode!=='string'||discountCode.length>64)throw Error('Invalid checkout request');
    opening=true;
    try{
      // The server validates the exact price and binds it to the signed-in user.
      // false uses a one-time price, not a recurring price to cancel later.
      const session=await gateway.checkout(plan,autoRenew);
      if(!session||typeof session.priceId!=='string'||typeof session.customData?.anastomosis_binding!=='string')throw Error('Invalid checkout session');
      const promo=discountCode.trim();
      const request={items:[{priceId:session.priceId,quantity:1}],customData:session.customData,...(promo?{discountCode:promo}:{})};
      paddle.Checkout.open(request);
      return{opened:true};
    }finally{opening=false;}
  }
  return{open};
}
