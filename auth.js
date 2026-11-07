import { account, ID } from "./appwrite.js";

export async function signUp(name, email, password) {
  await account.create(ID.unique(), email, password, name);
  await logIn(email, password);
}

export async function logIn(email, password) {
  await account.createEmailPasswordSession(email, password);
}

export async function logOut() {
  await account.deleteSession("current");
}

export async function getCurrentUser() {
  try {
    return await account.get();
  } catch (err) {
    return null;
  }
}

export async function sendPasswordReset(email) {
  const resetURL = new URL("reset-password.html", window.location.href).href;
  await account.createRecovery(email, resetURL);
}

export async function confirmPasswordReset(userId, secret, newPassword) {
  await account.updateRecovery(userId, secret, newPassword);
}
