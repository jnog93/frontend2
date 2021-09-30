/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
function t(t,e,i,n){var o,s=arguments.length,r=s<3?e:null===n?n=Object.getOwnPropertyDescriptor(e,i):n;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,i,n);else for(var a=t.length-1;a>=0;a--)(o=t[a])&&(r=(s<3?o(r):s>3?o(e,i,r):o(e,i))||r);return s>3&&r&&Object.defineProperty(e,i,r),r
/**
@license
Copyright 2020 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/}class e{constructor(t){this.startPress=e=>{t().then(t=>{t&&t.startPress(e)})},this.endPress=()=>{t().then(t=>{t&&t.endPress()})},this.startFocus=()=>{t().then(t=>{t&&t.startFocus()})},this.endFocus=()=>{t().then(t=>{t&&t.endFocus()})},this.startHover=()=>{t().then(t=>{t&&t.startHover()})},this.endHover=()=>{t().then(t=>{t&&t.endHover()})}}}
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const i=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,n=Symbol(),o=new Map;class s{constructor(t,e){if(this._$cssResult$=!0,e!==n)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t}get styleSheet(){let t=o.get(this.cssText);return i&&void 0===t&&(o.set(this.cssText,t=new CSSStyleSheet),t.replaceSync(this.cssText)),t}toString(){return this.cssText}}const r=t=>new s("string"==typeof t?t:t+"",n),a=(t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,n)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[n+1],t[0]);return new s(i,n)},l=(t,e)=>{i?t.adoptedStyleSheets=e.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet):e.forEach(e=>{const i=document.createElement("style"),n=window.litNonce;void 0!==n&&i.setAttribute("nonce",n),i.textContent=e.cssText,t.appendChild(i)})},c=i?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return r(e)})(t):t
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */;var h,d;const u={toAttribute(t,e){switch(e){case Boolean:t=t?"":null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},p=(t,e)=>e!==t&&(e==e||t==t),f={attribute:!0,type:String,converter:u,reflect:!1,hasChanged:p};class m extends HTMLElement{constructor(){super(),this._$Et=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Ei=null,this.o()}static addInitializer(t){var e;null!==(e=this.l)&&void 0!==e||(this.l=[]),this.l.push(t)}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach((e,i)=>{const n=this._$Eh(i,e);void 0!==n&&(this._$Eu.set(n,i),t.push(n))}),t}static createProperty(t,e=f){if(e.state&&(e.attribute=!1),this.finalize(),this.elementProperties.set(t,e),!e.noAccessor&&!this.prototype.hasOwnProperty(t)){const i="symbol"==typeof t?Symbol():"__"+t,n=this.getPropertyDescriptor(t,i,e);void 0!==n&&Object.defineProperty(this.prototype,t,n)}}static getPropertyDescriptor(t,e,i){return{get(){return this[e]},set(n){const o=this[t];this[e]=n,this.requestUpdate(t,o,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||f}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),this.elementProperties=new Map(t.elementProperties),this._$Eu=new Map,this.hasOwnProperty("properties")){const t=this.properties,e=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const i of e)this.createProperty(i,t[i])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(c(t))}else void 0!==t&&e.push(c(t));return e}static _$Eh(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}o(){var t;this._$Ev=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$Ep(),this.requestUpdate(),null===(t=this.constructor.l)||void 0===t||t.forEach(t=>t(this))}addController(t){var e,i;(null!==(e=this._$Em)&&void 0!==e?e:this._$Em=[]).push(t),void 0!==this.renderRoot&&this.isConnected&&(null===(i=t.hostConnected)||void 0===i||i.call(t))}removeController(t){var e;null===(e=this._$Em)||void 0===e||e.splice(this._$Em.indexOf(t)>>>0,1)}_$Ep(){this.constructor.elementProperties.forEach((t,e)=>{this.hasOwnProperty(e)&&(this._$Et.set(e,this[e]),delete this[e])})}createRenderRoot(){var t;const e=null!==(t=this.shadowRoot)&&void 0!==t?t:this.attachShadow(this.constructor.shadowRootOptions);return l(e,this.constructor.elementStyles),e}connectedCallback(){var t;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(t=this._$Em)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostConnected)||void 0===e?void 0:e.call(t)})}enableUpdating(t){}disconnectedCallback(){var t;null===(t=this._$Em)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostDisconnected)||void 0===e?void 0:e.call(t)})}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$Eg(t,e,i=f){var n,o;const s=this.constructor._$Eh(t,i);if(void 0!==s&&!0===i.reflect){const r=(null!==(o=null===(n=i.converter)||void 0===n?void 0:n.toAttribute)&&void 0!==o?o:u.toAttribute)(e,i.type);this._$Ei=t,null==r?this.removeAttribute(s):this.setAttribute(s,r),this._$Ei=null}}_$AK(t,e){var i,n,o;const s=this.constructor,r=s._$Eu.get(t);if(void 0!==r&&this._$Ei!==r){const t=s.getPropertyOptions(r),a=t.converter,l=null!==(o=null!==(n=null===(i=a)||void 0===i?void 0:i.fromAttribute)&&void 0!==n?n:"function"==typeof a?a:null)&&void 0!==o?o:u.fromAttribute;this._$Ei=r,this[r]=l(e,t.type),this._$Ei=null}}requestUpdate(t,e,i){let n=!0;void 0!==t&&(((i=i||this.constructor.getPropertyOptions(t)).hasChanged||p)(this[t],e)?(this._$AL.has(t)||this._$AL.set(t,e),!0===i.reflect&&this._$Ei!==t&&(void 0===this._$ES&&(this._$ES=new Map),this._$ES.set(t,i))):n=!1),!this.isUpdatePending&&n&&(this._$Ev=this._$EC())}async _$EC(){this.isUpdatePending=!0;try{await this._$Ev}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this._$Et&&(this._$Et.forEach((t,e)=>this[e]=t),this._$Et=void 0);let e=!1;const i=this._$AL;try{e=this.shouldUpdate(i),e?(this.willUpdate(i),null===(t=this._$Em)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostUpdate)||void 0===e?void 0:e.call(t)}),this.update(i)):this._$ET()}catch(t){throw e=!1,this._$ET(),t}e&&this._$AE(i)}willUpdate(t){}_$AE(t){var e;null===(e=this._$Em)||void 0===e||e.forEach(t=>{var e;return null===(e=t.hostUpdated)||void 0===e?void 0:e.call(t)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$ET(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$Ev}shouldUpdate(t){return!0}update(t){void 0!==this._$ES&&(this._$ES.forEach((t,e)=>this._$Eg(e,this[e],t)),this._$ES=void 0),this._$ET()}updated(t){}firstUpdated(t){}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var v,g;m.finalized=!0,m.elementProperties=new Map,m.elementStyles=[],m.shadowRootOptions={mode:"open"},null===(h=globalThis.reactiveElementPolyfillSupport)||void 0===h||h.call(globalThis,{ReactiveElement:m}),(null!==(d=globalThis.reactiveElementVersions)&&void 0!==d?d:globalThis.reactiveElementVersions=[]).push("1.0.0");const _=globalThis.trustedTypes,y=_?_.createPolicy("lit-html",{createHTML:t=>t}):void 0,$=`lit$${(Math.random()+"").slice(9)}$`,b="?"+$,w=`<${b}>`,A=document,S=(t="")=>A.createComment(t),E=t=>null===t||"object"!=typeof t&&"function"!=typeof t,x=Array.isArray,C=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,M=/-->/g,H=/>/g,k=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,T=/'/g,D=/"/g,P=/^(?:script|style|textarea)$/i,O=(t=>(e,...i)=>({_$litType$:t,strings:e,values:i}))(1),z=Symbol.for("lit-noChange"),N=Symbol.for("lit-nothing"),U=new WeakMap,R=A.createTreeWalker(A,129,null,!1),L=(t,e)=>{const i=t.length-1,n=[];let o,s=2===e?"<svg>":"",r=C;for(let e=0;e<i;e++){const i=t[e];let a,l,c=-1,h=0;for(;h<i.length&&(r.lastIndex=h,l=r.exec(i),null!==l);)h=r.lastIndex,r===C?"!--"===l[1]?r=M:void 0!==l[1]?r=H:void 0!==l[2]?(P.test(l[2])&&(o=RegExp("</"+l[2],"g")),r=k):void 0!==l[3]&&(r=k):r===k?">"===l[0]?(r=null!=o?o:C,c=-1):void 0===l[1]?c=-2:(c=r.lastIndex-l[2].length,a=l[1],r=void 0===l[3]?k:'"'===l[3]?D:T):r===D||r===T?r=k:r===M||r===H?r=C:(r=k,o=void 0);const d=r===k&&t[e+1].startsWith("/>")?" ":"";s+=r===C?i+w:c>=0?(n.push(a),i.slice(0,c)+"$lit$"+i.slice(c)+$+d):i+$+(-2===c?(n.push(void 0),e):d)}const a=s+(t[i]||"<?>")+(2===e?"</svg>":"");return[void 0!==y?y.createHTML(a):a,n]};class Y{constructor({strings:t,_$litType$:e},i){let n;this.parts=[];let o=0,s=0;const r=t.length-1,a=this.parts,[l,c]=L(t,e);if(this.el=Y.createElement(l,i),R.currentNode=this.el.content,2===e){const t=this.el.content,e=t.firstChild;e.remove(),t.append(...e.childNodes)}for(;null!==(n=R.nextNode())&&a.length<r;){if(1===n.nodeType){if(n.hasAttributes()){const t=[];for(const e of n.getAttributeNames())if(e.endsWith("$lit$")||e.startsWith($)){const i=c[s++];if(t.push(e),void 0!==i){const t=n.getAttribute(i.toLowerCase()+"$lit$").split($),e=/([.?@])?(.*)/.exec(i);a.push({type:1,index:o,name:e[2],strings:t,ctor:"."===e[1]?F:"?"===e[1]?q:"@"===e[1]?Z:B})}else a.push({type:6,index:o})}for(const e of t)n.removeAttribute(e)}if(P.test(n.tagName)){const t=n.textContent.split($),e=t.length-1;if(e>0){n.textContent=_?_.emptyScript:"";for(let i=0;i<e;i++)n.append(t[i],S()),R.nextNode(),a.push({type:2,index:++o});n.append(t[e],S())}}}else if(8===n.nodeType)if(n.data===b)a.push({type:2,index:o});else{let t=-1;for(;-1!==(t=n.data.indexOf($,t+1));)a.push({type:7,index:o}),t+=$.length-1}o++}}static createElement(t,e){const i=A.createElement("template");return i.innerHTML=t,i}}function j(t,e,i=t,n){var o,s,r,a;if(e===z)return e;let l=void 0!==n?null===(o=i._$Cl)||void 0===o?void 0:o[n]:i._$Cu;const c=E(e)?void 0:e._$litDirective$;return(null==l?void 0:l.constructor)!==c&&(null===(s=null==l?void 0:l._$AO)||void 0===s||s.call(l,!1),void 0===c?l=void 0:(l=new c(t),l._$AT(t,i,n)),void 0!==n?(null!==(r=(a=i)._$Cl)&&void 0!==r?r:a._$Cl=[])[n]=l:i._$Cu=l),void 0!==l&&(e=j(t,l._$AS(t,e.values),l,n)),e}class V{constructor(t,e){this.v=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}p(t){var e;const{el:{content:i},parts:n}=this._$AD,o=(null!==(e=null==t?void 0:t.creationScope)&&void 0!==e?e:A).importNode(i,!0);R.currentNode=o;let s=R.nextNode(),r=0,a=0,l=n[0];for(;void 0!==l;){if(r===l.index){let e;2===l.type?e=new I(s,s.nextSibling,this,t):1===l.type?e=new l.ctor(s,l.name,l.strings,this,t):6===l.type&&(e=new W(s,this,t)),this.v.push(e),l=n[++a]}r!==(null==l?void 0:l.index)&&(s=R.nextNode(),r++)}return o}m(t){let e=0;for(const i of this.v)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class I{constructor(t,e,i,n){var o;this.type=2,this._$AH=N,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=n,this._$Cg=null===(o=null==n?void 0:n.isConnected)||void 0===o||o}get _$AU(){var t,e;return null!==(e=null===(t=this._$AM)||void 0===t?void 0:t._$AU)&&void 0!==e?e:this._$Cg}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=j(this,t,e),E(t)?t===N||null==t||""===t?(this._$AH!==N&&this._$AR(),this._$AH=N):t!==this._$AH&&t!==z&&this.$(t):void 0!==t._$litType$?this.T(t):void 0!==t.nodeType?this.S(t):(t=>{var e;return x(t)||"function"==typeof(null===(e=t)||void 0===e?void 0:e[Symbol.iterator])})(t)?this.M(t):this.$(t)}A(t,e=this._$AB){return this._$AA.parentNode.insertBefore(t,e)}S(t){this._$AH!==t&&(this._$AR(),this._$AH=this.A(t))}$(t){this._$AH!==N&&E(this._$AH)?this._$AA.nextSibling.data=t:this.S(A.createTextNode(t)),this._$AH=t}T(t){var e;const{values:i,_$litType$:n}=t,o="number"==typeof n?this._$AC(t):(void 0===n.el&&(n.el=Y.createElement(n.h,this.options)),n);if((null===(e=this._$AH)||void 0===e?void 0:e._$AD)===o)this._$AH.m(i);else{const t=new V(o,this),e=t.p(this.options);t.m(i),this.S(e),this._$AH=t}}_$AC(t){let e=U.get(t.strings);return void 0===e&&U.set(t.strings,e=new Y(t)),e}M(t){x(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,n=0;for(const o of t)n===e.length?e.push(i=new I(this.A(S()),this.A(S()),this,this.options)):i=e[n],i._$AI(o),n++;n<e.length&&(this._$AR(i&&i._$AB.nextSibling,n),e.length=n)}_$AR(t=this._$AA.nextSibling,e){var i;for(null===(i=this._$AP)||void 0===i||i.call(this,!1,!0,e);t&&t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){var e;void 0===this._$AM&&(this._$Cg=t,null===(e=this._$AP)||void 0===e||e.call(this,t))}}class B{constructor(t,e,i,n,o){this.type=1,this._$AH=N,this._$AN=void 0,this.element=t,this.name=e,this._$AM=n,this.options=o,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=N}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(t,e=this,i,n){const o=this.strings;let s=!1;if(void 0===o)t=j(this,t,e,0),s=!E(t)||t!==this._$AH&&t!==z,s&&(this._$AH=t);else{const n=t;let r,a;for(t=o[0],r=0;r<o.length-1;r++)a=j(this,n[i+r],e,r),a===z&&(a=this._$AH[r]),s||(s=!E(a)||a!==this._$AH[r]),a===N?t=N:t!==N&&(t+=(null!=a?a:"")+o[r+1]),this._$AH[r]=a}s&&!n&&this.k(t)}k(t){t===N?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=t?t:"")}}class F extends B{constructor(){super(...arguments),this.type=3}k(t){this.element[this.name]=t===N?void 0:t}}class q extends B{constructor(){super(...arguments),this.type=4}k(t){t&&t!==N?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}class Z extends B{constructor(t,e,i,n,o){super(t,e,i,n,o),this.type=5}_$AI(t,e=this){var i;if((t=null!==(i=j(this,t,e,0))&&void 0!==i?i:N)===z)return;const n=this._$AH,o=t===N&&n!==N||t.capture!==n.capture||t.once!==n.once||t.passive!==n.passive,s=t!==N&&(n===N||o);o&&this.element.removeEventListener(this.name,this,n),s&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e,i;"function"==typeof this._$AH?this._$AH.call(null!==(i=null===(e=this.options)||void 0===e?void 0:e.host)&&void 0!==i?i:this.element,t):this._$AH.handleEvent(t)}}class W{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){j(this,t)}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var J,K,X;null===(v=globalThis.litHtmlPolyfillSupport)||void 0===v||v.call(globalThis,Y,I),(null!==(g=globalThis.litHtmlVersions)&&void 0!==g?g:globalThis.litHtmlVersions=[]).push("2.0.0");class G extends m{constructor(){super(...arguments),this.renderOptions={host:this},this._$Dt=void 0}createRenderRoot(){var t,e;const i=super.createRenderRoot();return null!==(t=(e=this.renderOptions).renderBefore)&&void 0!==t||(e.renderBefore=i.firstChild),i}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Dt=((t,e,i)=>{var n,o;const s=null!==(n=null==i?void 0:i.renderBefore)&&void 0!==n?n:e;let r=s._$litPart$;if(void 0===r){const t=null!==(o=null==i?void 0:i.renderBefore)&&void 0!==o?o:null;s._$litPart$=r=new I(e.insertBefore(S(),t),t,void 0,null!=i?i:{})}return r._$AI(t),r})(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),null===(t=this._$Dt)||void 0===t||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this._$Dt)||void 0===t||t.setConnected(!1)}render(){return z}}G.finalized=!0,G._$litElement$=!0,null===(J=globalThis.litElementHydrateSupport)||void 0===J||J.call(globalThis,{LitElement:G}),null===(K=globalThis.litElementPolyfillSupport)||void 0===K||K.call(globalThis,{LitElement:G}),(null!==(X=globalThis.litElementVersions)&&void 0!==X?X:globalThis.litElementVersions=[]).push("3.0.0");
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
String(Math.random()).slice(2),window.trustedTypes&&trustedTypes.createPolicy("lit-html",{createHTML:t=>t})
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
let Q=!1;(()=>{try{const t={get capture(){return Q=!0,!1}};window.addEventListener("test",t,t),window.removeEventListener("test",t,t)}catch(t){}})(),
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
"undefined"!=typeof window&&(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.4.1")
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */,void 0===window.ShadyCSS||void 0===window.ShadyCSS.prepareTemplateDom&&console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1.")
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */,window.JSCompiler_renameProperty=(t,e)=>t
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */;const tt=(t,e,i)=>{Object.defineProperty(e,i,t)},et=(t,e)=>({kind:"method",placement:"prototype",key:e.key,descriptor:t})
/**
@license
Copyright (c) 2019 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/;window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&CSSStyleSheet.prototype;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
(window.litElementVersions||(window.litElementVersions=[])).push("2.5.1");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const it=t=>e=>"function"==typeof e?((t,e)=>(window.customElements.define(t,e),e))(t,e):((t,e)=>{const{kind:i,elements:n}=e;return{kind:i,elements:n,finisher(e){window.customElements.define(t,e)}}})(t,e)
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */,nt=(t,e)=>"method"===e.kind&&e.descriptor&&!("value"in e.descriptor)?{...e,finisher(i){i.createProperty(e.key,t)}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:e.key,initializer(){"function"==typeof e.initializer&&(this[e.key]=e.initializer.call(this))},finisher(i){i.createProperty(e.key,t)}};function ot(t){return(e,i)=>void 0!==i?((t,e,i)=>{e.constructor.createProperty(i,t)})(t,e,i):nt(t,e)
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */}function st(t){return ot({...t,state:!0})}
/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const rt=t=>null!=t?t:N
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */,at=1,lt=t=>(...e)=>({_$litDirective$:t,values:e});class ct{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,i){this._$Ct=t,this._$AM=e,this._$Ci=i}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}}
/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const ht=lt(class extends ct{constructor(t){var e;if(super(t),t.type!==at||"class"!==t.name||(null===(e=t.strings)||void 0===e?void 0:e.length)>2)throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.")}render(t){return" "+Object.keys(t).filter(e=>t[e]).join(" ")+" "}update(t,[e]){var i,n;if(void 0===this.st){this.st=new Set,void 0!==t.strings&&(this.et=new Set(t.strings.join(" ").split(/\s/).filter(t=>""!==t)));for(const t in e)e[t]&&!(null===(i=this.et)||void 0===i?void 0:i.has(t))&&this.st.add(t);return this.render(e)}const o=t.element.classList;this.st.forEach(t=>{t in e||(o.remove(t),this.st.delete(t))});for(const t in e){const i=!!e[t];i===this.st.has(t)||(null===(n=this.et)||void 0===n?void 0:n.has(t))||(i?(o.add(t),this.st.add(t)):(o.remove(t),this.st.delete(t)))}return z}});var dt=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,ut="[^\\s]+",pt=/\[([^]*?)\]/gm;function ft(t,e){for(var i=[],n=0,o=t.length;n<o;n++)i.push(t[n].substr(0,e));return i}var mt=function(t){return function(e,i){var n=i[t].map((function(t){return t.toLowerCase()})).indexOf(e.toLowerCase());return n>-1?n:null}};function vt(t){for(var e=[],i=1;i<arguments.length;i++)e[i-1]=arguments[i];for(var n=0,o=e;n<o.length;n++){var s=o[n];for(var r in s)t[r]=s[r]}return t}var gt=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],_t=["January","February","March","April","May","June","July","August","September","October","November","December"],yt=ft(_t,3),$t={dayNamesShort:ft(gt,3),dayNames:gt,monthNamesShort:yt,monthNames:_t,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10?1:0)*t%10]}},bt=vt({},$t),wt=function(t,e){for(void 0===e&&(e=2),t=String(t);t.length<e;)t="0"+t;return t},At={D:function(t){return String(t.getDate())},DD:function(t){return wt(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return String(t.getDay())},dd:function(t){return wt(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return String(t.getMonth()+1)},MM:function(t){return wt(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return wt(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return wt(t.getFullYear(),4)},h:function(t){return String(t.getHours()%12||12)},hh:function(t){return wt(t.getHours()%12||12)},H:function(t){return String(t.getHours())},HH:function(t){return wt(t.getHours())},m:function(t){return String(t.getMinutes())},mm:function(t){return wt(t.getMinutes())},s:function(t){return String(t.getSeconds())},ss:function(t){return wt(t.getSeconds())},S:function(t){return String(Math.round(t.getMilliseconds()/100))},SS:function(t){return wt(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return wt(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+wt(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)},Z:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+wt(Math.floor(Math.abs(e)/60),2)+":"+wt(Math.abs(e)%60,2)}},St=function(t){return+t-1},Et=[null,"[1-9]\\d?"],xt=[null,ut],Ct=["isPm",ut,function(t,e){var i=t.toLowerCase();return i===e.amPm[0]?0:i===e.amPm[1]?1:null}],Mt=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(t){var e=(t+"").match(/([+-]|\d\d)/gi);if(e){var i=60*+e[1]+parseInt(e[2],10);return"+"===e[0]?i:-i}return 0}],Ht=(mt("monthNamesShort"),mt("monthNames"),{default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",isoDate:"YYYY-MM-DD",isoDateTime:"YYYY-MM-DDTHH:mm:ssZ",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"});var kt,Tt,Dt=function(t,e,i){if(void 0===e&&(e=Ht.default),void 0===i&&(i={}),"number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date pass to format");var n=[];e=(e=Ht[e]||e).replace(pt,(function(t,e){return n.push(e),"@@@"}));var o=vt(vt({},bt),i);return(e=e.replace(dt,(function(e){return At[e](t,o)}))).replace(/@@@/g,(function(){return n.shift()}))};(function(){try{(new Date).toLocaleDateString("i")}catch(t){return"RangeError"===t.name}})(),function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}}(),function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}}();function Pt(t){return t.substr(0,t.indexOf("."))}!function(t){t.language="language",t.system="system",t.comma_decimal="comma_decimal",t.decimal_comma="decimal_comma",t.space_comma="space_comma",t.none="none"}(kt||(kt={})),function(t){t.language="language",t.system="system",t.am_pm="12",t.twenty_four="24"}(Tt||(Tt={}));var Ot=["closed","locked","off"],zt=function(t,e,i,n){n=n||{},i=null==i?{}:i;var o=new Event(e,{bubbles:void 0===n.bubbles||n.bubbles,cancelable:Boolean(n.cancelable),composed:void 0===n.composed||n.composed});return o.detail=i,t.dispatchEvent(o),o},Nt=function(t){zt(window,"haptic",t)},Ut=function(t,e){return function(t,e,i){void 0===i&&(i=!0);var n,o=Pt(e),s="group"===o?"homeassistant":o;switch(o){case"lock":n=i?"unlock":"lock";break;case"cover":n=i?"open_cover":"close_cover";break;default:n=i?"turn_on":"turn_off"}return t.callService(s,n,{entity_id:e})}(t,e,Ot.includes(t.states[e].state))},Rt=function(t,e,i,n){if(n||(n={action:"more-info"}),!n.confirmation||n.confirmation.exemptions&&n.confirmation.exemptions.some((function(t){return t.user===e.user.id}))||(Nt("warning"),confirm(n.confirmation.text||"Are you sure you want to "+n.action+"?")))switch(n.action){case"more-info":(i.entity||i.camera_image)&&zt(t,"hass-more-info",{entityId:i.entity?i.entity:i.camera_image});break;case"navigate":n.navigation_path&&function(t,e,i){void 0===i&&(i=!1),i?history.replaceState(null,"",e):history.pushState(null,"",e),zt(window,"location-changed",{replace:i})}(0,n.navigation_path);break;case"url":n.url_path&&window.open(n.url_path);break;case"toggle":i.entity&&(Ut(e,i.entity),Nt("success"));break;case"call-service":if(!n.service)return void Nt("failure");var o=n.service.split(".",2);e.callService(o[0],o[1],n.service_data),Nt("success");break;case"fire-dom-event":zt(t,"ll-custom",n)}};function Lt(t){return void 0!==t&&"none"!==t.action}const Yt=["switch","light"];let jt=class extends G{constructor(){super(...arguments),this._initialized=!1}setConfig(t){this._config=t,this.loadCardHelpers()}shouldUpdate(){return this._initialized||this._initialize(),!0}get _name(){var t;return(null===(t=this._config)||void 0===t?void 0:t.name)||""}get _show_name(){var t,e;return null===(e=null===(t=this._config)||void 0===t?void 0:t.show_name)||void 0===e||e}get _show_state(){var t,e;return null===(e=null===(t=this._config)||void 0===t?void 0:t.show_state)||void 0===e||e}get _entity(){var t;return(null===(t=this._config)||void 0===t?void 0:t.entity)||""}get _show_warning(){var t;return(null===(t=this._config)||void 0===t?void 0:t.show_warning)||!1}get _show_error(){var t;return(null===(t=this._config)||void 0===t?void 0:t.show_error)||!1}get _tap_action(){var t;return(null===(t=this._config)||void 0===t?void 0:t.tap_action)||{action:"more-info"}}get _hold_action(){var t;return(null===(t=this._config)||void 0===t?void 0:t.hold_action)||{action:"none"}}get _double_tap_action(){var t;return(null===(t=this._config)||void 0===t?void 0:t.double_tap_action)||{action:"none"}}render(){if(!this.hass||!this._helpers)return O``;this._helpers.importMoreInfoControl("climate");Object.keys(this.hass.states).filter(t=>"switch"===t.substr(0,t.indexOf(".")));return O`
      <div class="card-config">
        <div class="option" .option=${"required"}>
          <ha-entity-picker
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.entity")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .hass=${this.hass}
            .value=${this._entity}
            .configValue=${"entity"}
            .includeDomains=${Yt}
            @value-changed=${this._valueChanged}
            allow-custom-entity>
          </ha-entity-picker>

      <div class="side-by-side">
          <paper-input
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.name")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .value=${this._name}
            .configValue=${"name"}
            @value-changed=${this._valueChanged}>
          </paper-input>
      </div class="side-by-side">

      <div class="div-options">
          <ha-formfield
            .label=${this.hass.localize("ui.panel.lovelace.editor.card.generic.show_name")}
            .dir=${this.dir}>
          <ha-switch
            .checked=${!1!==this._show_name}
            .configValue=${"show_name"}
            @change=${this._change}>
          </ha-switch>
          </ha-formfield>

          <ha-formfield
            .label=${this.hass.localize("ui.panel.lovelace.editor.card.generic.show_state")}
            .dir=${this.dir}>
          <ha-switch
            .checked=${!1!==this._show_state}
            .configValue=${"show_state"}
            @change=${this._change}>
          </ha-switch>
          </ha-formfield>

        <paper-dropdown-menu>
          <paper-listbox slot="dropdown-content"
            attr-for-selected="value"
            .configValue=${"icon"}
            selected='1'
            @iron-select=${this._changed_icon}>
            ${["mdi:ceiling-light","mdi:floor-lamp"].sort().map(t=>O` <paper-item value=${t}><ha-icon .icon=${t}></ha-icon>${t.split(":")[1]}</paper-item>`)}

          <paper-item .value=${["M27.4 47.3h-4.9s-.7.1-.7.8.4.9.7.9h4.9c.3 0 .7-.1.7-.9s-.7-.8-.7-.8zm3.3-2.9H19.3s-.8 0-.8.8.6.9.8.9h11.5c.2 0 .8-.1.8-.9-.1-.8-.9-.8-.9-.8zm0-3H19.3s-.8 0-.8.8.6.9.8.9h11.5c.2 0 .8-.1.8-.9-.1-.8-.9-.8-.9-.8zm0-2.9H19.3s-.8 0-.8.8.6.9.8.9h11.5c.2 0 .8-.1.8-.9s-.9-.8-.9-.8zm5.2-23.2c-3.3-5.3-7-5.6-10.9-5.6-3.8 0-8.4.4-10.9 5.6-.1.1-.1.3.1.7.4.8 3.3 7.2 3.2 18.8 0 1.1-.1 1.6 0 1.7 0 .1 0 .7 1.1.7h13c1 0 1-.5 1.1-.7v-1.7c-.1-11.6 2.8-18 3.2-18.8.1-.4.1-.5.1-.7","M14.1 15.3c3.4-.3 7-.4 10.9-.4 3.8 0 7.5.2 10.9.4.4-.4.7-.8.9-1.1C39 8.5 38.9 6.5 38.9 6c-.2-4.4-8.4-5-12.1-5h0-3.4c-3.7 0-12 .5-12.1 5 0 .5-.1 2.5 2.1 8.2 0 .3.3.8.7 1.1z"]}>
              <svg viewBox="0 0 50 50" height="24" width="24" >
              <path fill="#ffffff" d="M27.4 47.3h-4.9s-.7.1-.7.8.4.9.7.9h4.9c.3 0 .7-.1.7-.9s-.7-.8-.7-.8zm3.3-2.9H19.3s-.8 0-.8.8.6.9.8.9h11.5c.2 0 .8-.1.8-.9-.1-.8-.9-.8-.9-.8zm0-3H19.3s-.8 0-.8.8.6.9.8.9h11.5c.2 0 .8-.1.8-.9-.1-.8-.9-.8-.9-.8zm0-2.9H19.3s-.8 0-.8.8.6.9.8.9h11.5c.2 0 .8-.1.8-.9s-.9-.8-.9-.8zm5.2-23.2c-3.3-5.3-7-5.6-10.9-5.6-3.8 0-8.4.4-10.9 5.6-.1.1-.1.3.1.7.4.8 3.3 7.2 3.2 18.8 0 1.1-.1 1.6 0 1.7 0 .1 0 .7 1.1.7h13c1 0 1-.5 1.1-.7v-1.7c-.1-11.6 2.8-18 3.2-18.8.1-.4.1-.5.1-.7"/>
              <path d="M14.1 15.3c3.4-.3 7-.4 10.9-.4 3.8 0 7.5.2 10.9.4.4-.4.7-.8.9-1.1C39 8.5 38.9 6.5 38.9 6c-.2-4.4-8.4-5-12.1-5h0-3.4c-3.7 0-12 .5-12.1 5 0 .5-.1 2.5 2.1 8.2 0 .3.3.8.7 1.1z"/>
              </svg>Raceland Lâmpada
          </paper-item>

          <paper-item .value=${["M26.5 21.8l3.8-6.1H19.7l3.8 6.1c-5 .7-6.3 5.8-5.7 10.2.7 5.1 3.2 10.1 5.7 14.4H19v2.5h11.8v-2.5h-4.5C29 42 31.4 37 32.1 32c.6-4.4-.6-9.4-5.6-10.2zm3.1 9.1c-.3 4.3-2.3 8.7-4.4 12.4l-.2.1v.1-.1c-1.8-3-3.3-6.4-4.1-9.7-.7-3.1-1-7.2 2.7-8.4 1.4-.5 3.1-.1 4.2.8 1.6 1 1.8 3 1.8 4.8z","M38.1 20L35.7 3.8c-.3-1.9-.4-1.7-.6-2-.9-.6-2.3-.7-2.3-.7H17.4s-1.4 0-2.3.7c-.2.3-.3.1-.6 2C14 5.7 11.9 20 11.9 20s5.8.3 13.4.3h0c7.3 0 12.8-.3 12.8-.3z"]}>
              <svg viewBox="0 0 50 50" height="24" width="24" >
              <path fill="#000000" d="M38.1 20L35.7 3.8c-.3-1.9-.4-1.7-.6-2-.9-.6-2.3-.7-2.3-.7H17.4s-1.4 0-2.3.7c-.2.3-.3.1-.6 2C14 5.7 11.9 20 11.9 20s5.8.3 13.4.3h0c7.3 0 12.8-.3 12.8-.3z"/>
              <path fill="#ffffff" d="M26.5 21.8l3.8-6.1H19.7l3.8 6.1c-5 .7-6.3 5.8-5.7 10.2.7 5.1 3.2 10.1 5.7 14.4H19v2.5h11.8v-2.5h-4.5C29 42 31.4 37 32.1 32c.6-4.4-.6-9.4-5.6-10.2zm3.1 9.1c-.3 4.3-2.3 8.7-4.4 12.4l-.2.1v.1-.1c-1.8-3-3.3-6.4-4.1-9.7-.7-3.1-1-7.2 2.7-8.4 1.4-.5 3.1-.1 4.2.8 1.6 1 1.8 3 1.8 4.8z"/>
              </svg>Raceland Candeeiro
          </paper-item>

          </paper-listbox>
        </paper-dropdown-menu>
        </div>
    </div>
    </div>
    `}_change(t){if(!this._config||!this.hass)return;const e=t.target,i=e.checked;this["_"+e.configValue]!==i&&zt(this,"config-changed",{config:Object.assign(Object.assign({},this._config),{[e.configValue]:i})})}_initialize(){void 0!==this.hass&&void 0!==this._config&&void 0!==this._helpers&&(this._initialized=!0)}async loadCardHelpers(){this._helpers=await window.loadCardHelpers()}_valueChanged(t){if(!this._config||!this.hass)return;const e=t.target;if(this["_"+e.configValue]!==e.value){if(e.configValue)if(""===e.value){const t=Object.assign({},this._config);delete t[e.configValue],this._config=t}else this._config=Object.assign(Object.assign({},this._config),{[e.configValue]:void 0!==e.checked?e.checked:e.value});zt(this,"config-changed",{config:this._config})}}_changed_icon(t){this.hass&&""!==t.target.selected&&(this._config=Object.assign(Object.assign({},this._config),{[t.target.configValue]:t.target.selected,type:"custom:light-card"}),zt(this,"config-changed",{config:this._config}))}static get styles(){return a`
      .option {
        padding: 4px 0px;
        cursor: pointer;
      }
      .row {
        display: flex;
        margin-bottom: -14px;
        pointer-events: none;
      }
      .title {
        padding-left: 16px;
        margin-top: -6px;
        pointer-events: none;
      }
      .secondary {
        padding-left: 40px;
        color: var(--secondary-text-color);
        pointer-events: none;
      }
      .values {
        padding-left: 16px;
        background: var(--secondary-background-color);
        display: grid;
      }
      ha-formfield {
        padding: 0px 10px 0px 20px;
      }
    `}};t([ot({attribute:!1})],jt.prototype,"hass",void 0),t([st()],jt.prototype,"_config",void 0),t([ot()],jt.prototype,"icon_value",void 0),t([st()],jt.prototype,"_toggle",void 0),t([st()],jt.prototype,"_helpers",void 0),jt=t([it("light-card-editor")],jt);const Vt="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.maxTouchPoints>0;class It extends HTMLElement{constructor(){super(),this.holdTime=500,this.held=!1,this.ripple=document.createElement("mwc-ripple")}connectedCallback(){Object.assign(this.style,{position:"absolute",width:Vt?"100px":"50px",height:Vt?"100px":"50px",transform:"translate(-50%, -50%)",pointerEvents:"none",zIndex:"999"}),this.appendChild(this.ripple),this.ripple.primary=!0,["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach(t=>{document.addEventListener(t,()=>{clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0},{passive:!0})})}bind(t,e){if(t.actionHandler)return;t.actionHandler=!0,t.addEventListener("contextmenu",t=>{const e=t||window.event;return e.preventDefault&&e.preventDefault(),e.stopPropagation&&e.stopPropagation(),e.cancelBubble=!0,e.returnValue=!1,!1});const i=t=>{let e,i;this.held=!1,t.touches?(e=t.touches[0].pageX,i=t.touches[0].pageY):(e=t.pageX,i=t.pageY),this.timer=window.setTimeout(()=>{this.startAnimation(e,i),this.held=!0},this.holdTime)},n=i=>{i.preventDefault(),["touchend","touchcancel"].includes(i.type)&&void 0===this.timer||(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0,this.held?zt(t,"action",{action:"hold"}):e.hasDoubleClick?"click"===i.type&&i.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout(()=>{this.dblClickTimeout=void 0,zt(t,"action",{action:"tap"})},250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,zt(t,"action",{action:"double_tap"})):zt(t,"action",{action:"tap"}))};t.addEventListener("touchstart",i,{passive:!0}),t.addEventListener("touchend",n),t.addEventListener("touchcancel",n),t.addEventListener("mousedown",i,{passive:!0}),t.addEventListener("click",n),t.addEventListener("keyup",t=>{13===t.keyCode&&n(t)})}startAnimation(t,e){Object.assign(this.style,{left:t+"px",top:e+"px",display:null}),this.ripple.disabled=!1,this.ripple.active=!0,this.ripple.unbounded=!0}stopAnimation(){this.ripple.active=!1,this.ripple.disabled=!0,this.style.display="none"}}customElements.define("action-handler-light-card",It);const Bt=(t,e)=>{const i=(()=>{const t=document.body;if(t.querySelector("action-handler-light-card"))return t.querySelector("action-handler-light-card");const e=document.createElement("action-handler-light-card");return t.appendChild(e),e})();i&&i.bind(t,e)},Ft=lt(class extends ct{update(t,[e]){return Bt(t.element,e),z}render(t){}});var qt={version:"Version",invalid_configuration:"Invalid configuration",show_warning:"Show Warning",show_error:"Show Error"},Zt={on:"Ligado",off:"Desligado"},Wt={common:qt,states:Zt},Jt={version:"Versão",invalid_configuration:"Configuração Inválida",show_warning:"Mostrar Aviso",show_error:"Mostrar Erro"},Kt={on:"Ligado",off:"Desligado"},Xt={common:Jt,states:Kt};const Gt={en:Object.freeze({__proto__:null,common:qt,states:Zt,default:Wt}),pt:Object.freeze({__proto__:null,common:Jt,states:Kt,default:Xt})};function Qt(t,e="",i=""){const n=(localStorage.getItem("selectedLanguage")||"en").replace(/['"]+/g,"").replace("-","_");let o;try{o=t.split(".").reduce((t,e)=>t[e],Gt[n])}catch(e){o=t.split(".").reduce((t,e)=>t[e],Gt.en)}return void 0===o&&(o=t.split(".").reduce((t,e)=>t[e],Gt.en)),""!==e&&""!==i&&(o=o.replace(e,i)),o}console.info(`%c  RACELAND-light-card \n%c  ${Qt("common.version")} 1.4.0    `,"color: orange; font-weight: bold; background: black","color: white; font-weight: bold; background: dimgray"),window.customCards=window.customCards||[],window.customCards.push({type:"light-card",name:"light-card",preview:!0,description:"A light card custom card"});let te=class extends G{constructor(){super(...arguments),this.computeActiveState=t=>{const e=t.entity_id.split(".")[0];let i=t.state;return"climate"===e&&(i=t.attributes.hvac_action),i},this.computeObjectId=t=>t.substr(t.indexOf(".")+1),this.computeStateName=t=>void 0===t.attributes.friendly_name?this.computeObjectId(t.entity_id).replace(/_/g," "):t.attributes.friendly_name||"",this._rippleHandlers=new e(()=>this._ripple)}static async getConfigElement(){return document.createElement("light-card-editor")}static getStubConfig(){return{type:"custom:light-card",entity:"light.raceland",show_name:!0,show_state:!0,name:"raceland"}}setConfig(t){if(!t)throw new Error(Qt("common.invalidconfiguration"));t.test_gui&&function(){var t=document.querySelector("home-assistant");if(t=(t=(t=(t=(t=(t=(t=(t=t&&t.shadowRoot)&&t.querySelector("home-assistant-main"))&&t.shadowRoot)&&t.querySelector("app-drawer-layout partial-panel-resolver"))&&t.shadowRoot||t)&&t.querySelector("ha-panel-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-root")){var e=t.lovelace;return e.current_view=t.___curView,e}return null}().setEditMode(!0),this.config=Object.assign(Object.assign({show_icon:!0,icon:"mdi:floor-lamp"},t),{tap_action:{action:"toggle"}})}translate_state(t){return"on"===rt(t?this.computeActiveState(t):void 0)?Qt("states.on"):"off"===rt(t?this.computeActiveState(t):void 0)?Qt("states.off"):"unavailable"===rt(t?this.computeActiveState(t):void 0)?Qt("states.unavailable"):""}shouldUpdate(t){return!!this.config&&function(t,e,i){if(e.has("config")||i)return!0;if(t.config.entity){var n=e.get("hass");return!n||n.states[t.config.entity]!==t.hass.states[t.config.entity]}return!1}(this,t,!1)}render(){if(this.config.show_warning)return this._showWarning(Qt("common.show_warning"));if(this.config.show_error)return this._showError(Qt("common.show_error"));const t=this.config.entity?this.hass.states[this.config.entity]:void 0;return O`
      <ha-card
        class="hassbut ${ht({"state-on":"on"===rt(t?this.computeActiveState(t):void 0),"state-off":"off"===rt(t?this.computeActiveState(t):void 0)})}"
        @action=${this._handleAction}
        @focus="${this.handleRippleFocus}"
        .actionHandler=${Ft({hasHold:Lt(this.config.hold_action),hasDoubleClick:Lt(this.config.double_tap_action)})}
        tabindex="0"
        .label=${"fan: "+(this.config.entity||"No Entity Defined")}
      >
        ${this.config.show_icon?this.renderIcon(t):""}

        <div></div>
        ${this.config.show_name?O`
              <div tabindex="-1" class="name-div">${this.config.name}</div>
            `:""}
        <div></div>

        ${this.config.show_state?O`
              <div tabindex="-1" class="state-div">
                ${this.translate_state(t)}
                <div class="position"></div>
              </div>
            `:""}
        <div></div>
      </ha-card>
    `}renderIcon(t){return"string"==typeof this.config.icon?O`
      <ha-icon
      class="light-icon ${ht({"state-on-ceiling-light":"on"===rt(t?this.computeActiveState(t):void 0)&&"mdi:ceiling-light"===this.config.icon,"state-on-floor-lamp":"on"===rt(t?this.computeActiveState(t):void 0)&&"mdi:floor-lamp"===this.config.icon,"state-off":"off"===rt(t?this.computeActiveState(t):void 0),"state-unavailable":"unavailable"===rt(t?this.computeActiveState(t):void 0)})}"
      tabindex="-1"
      data-domain=${rt(this.config.state_color&&t?function(t){return Pt(t.entity_id)}(t):void 0)}
      data-state=${rt(t?this.computeActiveState(t):void 0)}
      .icon=${this.config.icon}
    ></ha-icon>`:!0===Array.isArray(this.config.icon)?O`
      <svg viewBox="0 0 50 50" height="100%" width="50%">
  <path fill="#ffffff" d=${this.config.icon[0]} />
  <path class=${ht({"state-on-light-icon":"on"===rt(t?this.computeActiveState(t):void 0),"state-off":"off"===rt(t?this.computeActiveState(t):void 0),"state-unavailable":"unavailable"===rt(t?this.computeActiveState(t):void 0)})}
  d=${this.config.icon[1]} />

</svg>`:""}_handleAction(t){this.hass&&this.config&&t.detail.action&&function(t,e,i,n){var o;"double_tap"===n&&i.double_tap_action?o=i.double_tap_action:"hold"===n&&i.hold_action?o=i.hold_action:"tap"===n&&i.tap_action&&(o=i.tap_action),Rt(t,e,i,o)}(this,this.hass,this.config,t.detail.action)}_showWarning(t){return O` <hui-warning>${t}</hui-warning> `}_showError(t){const e=document.createElement("hui-error-card");return e.setConfig({type:"error",error:t,origConfig:this.config}),O` ${e} `}handleRippleFocus(){this._rippleHandlers.startFocus()}static get styles(){return a`
      ha-card {
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 4% 0;
        font-size: 1.2rem;
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        justify-content: center;
        position: relative;
        background: rgba(120,120,120,0.7);
        color: white;
        border-radius: 25px;
        padding-left: 10%;
        padding-top: 15%;
        padding-bottom: 8%;

      }
      ha-card:focus {
        outline: solid;
        outline-color: white;
      }
      ha-icon {
        width: 50%;
        /* border: 2px solid #73AD21; */
        height: auto;
        padding: 0px 0px 0px 0px;
        color: var(--paper-item-icon-color, #44739e);
        --mdc-icon-size: 100%;
      }
      ha-icon + span {
        margin-top: 3%;
        margin-bottom: 10%;
      }
      ha-icon,
      span {
        outline: none;
      }
      .hassbut.state-on {
        background: rgba(255,255,255,0.7);
        color: black;
      }
      .hassbut {
        display: grid;
        grid-template-columns: 50% 50%;
      }
      .state-div {
        /* border: 2px solid #73AD21; */
        margin: 5% 0% 10% 0%;
        padding: 0px 0px 0px 0px;
        text-align: left;
        width: 100%;
      }
      .name-div {
        /* border: 2px solid #73AD21; */
        margin: 30% 25% 0% 0%;
        padding: 9% 0px 0px 0px;
        text-align: left;
        width: 100%;
      }
      .light-icon {
        transform: translate(0%, 0%);
      }
      .light-icon.state-on-ceiling-light {
        color: var(--paper-item-icon-active-color, #fdd835);
        animation: shake 0.9s;
        animation-iteration-count: 1;
      }
      .light-icon.state-on-floor-lamp {
        color: var(--paper-item-icon-active-color, #fdd835);
        animation: shaker 0.9s;
        animation-iteration-count: 1;
      }
      .state-on-light-icon {
        fill: var(--paper-item-icon-active-color, #fdd835);
        animation: shakerd 0.8s;
        transform-origin: center;
      }
      .state-on-light-lamp {
        fill: var(--paper-item-icon-active-color, #fdd835);
        animation: shakerdl 0.8s;
        transform-origin: center;
      }
      .light-icon.state-unavailable {
        color: var(--state-icon-unavailable-color, #bdbdbd);
      }
      @keyframes shake {
        0% { transform: rotate(0deg); }
        10% { transform: rotate(25deg); }
        20% { transform: rotate(0deg); }
        30% { transform: rotate(-25deg); }
        40% { transform: rotate(0deg); }
        50% { transform: rotate(25deg); }
        60% { transform: rotate(0deg); }
        70% { transform: rotate(-25deg); }
        80% { transform: rotate(0deg); }
        90% { transform: rotate(25deg); }
        100% { transform: rotate(0deg); }
      }
      @keyframes shaker {
        0% { transform: translate(0px); }
        25% { transform: translate(10px); }
        50% { transform: translate(0px); }
        75% { transform: translate(10px); }
        100% { transform: translate(0px); }
      }
      @keyframes shakerd {
        0% { transform: scale(0.85); }
        20% { transform: scale(1.1); }
        40% { transform: scale(0.95); }
        60% { transform: scale(1.03); }
        80% { transform: scale(0.97); }
        100% { transform: scale(1); }
      }
      @keyframes shakerdl {
        0% { transform: scale(0.85); }
        20% { transform: scale(1.1); }
        40% { transform: scale(0.95); }
        60% { transform: scale(1.03); }
        80% { transform: scale(0.97); }
        100% { transform: scale(1); }
      }
      .state {
        font-size: 0.9rem;
        color: var(--secondary-text-color);
      }
    `}};var ee;t([(ee="mwc-ripple",(t,e)=>{const i={async get(){return await this.updateComplete,this.renderRoot.querySelector(ee)},enumerable:!0,configurable:!0};return void 0!==e?tt(i,t,e):et(i,t)})],te.prototype,"_ripple",void 0),t([ot({attribute:!1})],te.prototype,"hass",void 0),t([st()],te.prototype,"config",void 0),te=t([it("light-card")],te);export{te as BoilerplateCard};
