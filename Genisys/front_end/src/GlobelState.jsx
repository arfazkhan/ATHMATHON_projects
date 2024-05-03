import { atom } from "jotai";
export const taskAtom = atom({
  task: 0,
  reward: 0,
  category: 0,
  expire: 0,
});

export const triggerAtom = atom(true);
