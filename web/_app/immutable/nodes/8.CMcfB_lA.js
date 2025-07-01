import{a as u,t as g}from"../chunks/7cevignt.js";import{p as h,b as a,z as w,a as x,d as y,g as r,c as v,r as D}from"../chunks/CF1GH9sA.js";import{h as b}from"../chunks/BHxXLP30.js";import{p as _,a as o}from"../chunks/CO6i_yYG.js";import{s as V,a as M}from"../chunks/4176nlKj.js";import{o as I}from"../chunks/TrLs3O3_.js";import{a as P}from"../chunks/D9TuCHYl.js";var S=g('<div id="_display_container_" class="h-full w-full svelte-1ucu3r2"><!></div>');function z(l,n){h(n,!0);const[d,c]=V(),p=()=>M(P,"$sideViewVisible",d);let s=y(`<div class="flex flex-col items-center h-full mt-48">
            <h1
                class="font-semibold font-arista text-4xl text-center text-surface-500 p-8 tracking-wide"
            >
                Welcome to MastroGPT
            </h1>
            <p class="text-lg">
                Please select the chat you want to use in the menu.
            </p>
        </div>`);const f=`<div class="flex flex-col items-center h-full mt-48">
            <h1
                class="font-semibold font-arista text-4xl text-center text-surface-500 p-8 tracking-wide"
            >
                Welcome to MastroGPT
            </h1>
            <p class="text-lg">
                Please select the chat you want to use in the menu.
            </p>
        </div>`;_(n,"displayResponse",15)(e=>{e&&(a(s,o(e)),typeof window<"u"&&sessionStorage.setItem("currentDisplayData",e))}),I(()=>{if(typeof window<"u"){const t=sessionStorage.getItem("currentDisplayData");t&&a(s,o(t))}const e=t=>{t.data&&typeof t.data=="string"&&(a(s,o(t.data)),sessionStorage.setItem("currentDisplayData",t.data))};return window.addEventListener("message",e),()=>{window.removeEventListener("message",e)}}),w(()=>{if(p()&&typeof window<"u"){const e=sessionStorage.getItem("currentDisplayData");e&&r(s)===f&&a(s,o(e))}});var i=S(),m=v(i);b(m,()=>r(s)),D(i),u(l,i),x(),c()}export{z as component};
