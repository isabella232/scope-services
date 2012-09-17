/**
 *
 * Copyright (c) 2008, Opera Software ASA
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, 
 * with or without modification, are permitted provided 
 * that the following conditions are met:
 *
 *  - Redistributions of source code must retain the above copyright notice, 
 *    this list of conditions and the following disclaimer.
 *
 *  - Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 *  - Neither the name of Opera Software nor the names of its contributors 
 *    may be used to endorse or promote products derived from this software 
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 * 
 **/



function markup(text){var kmap={};var keys=[];text=text.replace(/</g,"&lt;");text=text.replace(/("[^"]*")/g,'<span class="string">$1</span>');text=text.replace(/(#.*)/g,'<span class="comment">$1</span>');text=text.replace(/TODO/g,'<span class="not-started">TODO</span>');text=text.replace(/[A-Z][-A-Z0-9]{2,}(?=\s+::=)/g,function(key){if(!kmap.hasOwnProperty(key)){kmap[key]=true;keys.push(key);}
return "<a name=\"@"+key+"@\"></a>@"+key+"@";});keys.sort(function(a,b){return b.length-a.length;});for(var i=0;i<keys.length;i++)
text=text.replace(new RegExp("([^@][A-Z0-9-]*)("+keys[i]+")(?!(?:\"|@|-|[A-Z0-9-]))","g"),"$1<a href=\"#@$2@\">@$2@</a>");text=text.replace(/@/g,"");text=text.replace(/(http:\/\/[^\r\n\<\&]*)/g,'<a href="$1">$1</a>');return text;}
function scrollToHash(){var identifier=location.hash.replace(/^#/,'');if(identifier){var as=document.getElementsByTagName('a'),a=null,i=0;for(;a=as[i];i++){if(a.name==identifier){a.scrollIntoView();return;}}}}
function markup_grammar(){var grammar_elm=document.getElementById("grammar");if(grammar_elm){grammar_elm.innerHTML=markup(grammar_elm.innerText);scrollToHash();}}
