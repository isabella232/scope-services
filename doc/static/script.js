(function()
{
  if (!Element.prototype.matchesSelector)
  {
    Element.prototype.matchesSelector =
      Element.prototype.oMatchesSelector ?
      Element.prototype.oMatchesSelector :
      function(selector)
      {
        var sel = this.parentNode.querySelectorAll(selector);
        for (var i = 0; sel[i] && sel[i] != this; i++);
        return Boolean(sel[i]);
      }
  };

  /* The naming is not precise, it can return the element itself. */
  Element.prototype.get_ancestor = function(selector)
  {
    var ele = this;
    while (ele)
    {
      if (ele.matchesSelector(selector))
        return ele;
      ele = ele.parentElement;
    }
    return null;
  };

  var for_each = Function.prototype.call.bind(Array.prototype.forEach);
  var h1_height = 0;
  var side_panel = null;
  var side_panel_top = -1;

  var set_sidepanel_top = function()
  {
    var scroll_top = document.documentElement.scrollTop || document.body.scrollTop;
    var top = scroll_top > h1_height ? 0 : h1_height - scroll_top;
    if (top != side_panel_top)
    {
      side_panel_top = top;
      side_panel.style.top = top + "px";
    }
  };

  window.onload = function()
  {
    var h1 = document.querySelector("h1");
    h1_height = h1 && parseInt(h1.offsetHeight);
    side_panel = document.querySelector(".sphinxsidebar");
    set_sidepanel_top();
    window.addEventListener("scroll", set_sidepanel_top, false);
  };
})();
