// INCOMPLETE / DO NOT DEPLOY. This intentionally fails closed when disabled; enabling it before migration
// and backend testing is unsafe.
// Function IDs and price IDs are public identifiers, NOT API keys or secrets.
export const SECURE_CONFIG={
  enabled:false,
  questionFunctionId:'', checkoutFunctionId:'', accessFunctionId:'',
  priceIds:{
    monthly:{oneTime:'',recurring:'pri_01kxgfap9cs231vrkcyhcd055t'},
    threeMonth:{oneTime:'',recurring:'pri_01kxgfe4kvnx3jh70fd9xzkybw'},
    annual:{oneTime:'',recurring:'pri_01kxgfj20d6k3527bb1qtht0fk'}
  }
};
