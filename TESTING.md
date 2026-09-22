# The Heart of Ruritania - Testing

Validation of HTML, CSS, JS, Python

Lighthouse

## HTML and CSS validation

This is handled automatically as part of the Python testing.

To demonstrate that it does something, this is the output of a previously failing test:

```
FAIL: test_validate_page_edit_dish (menu.test_valid.TestValidPages.test_validate_page_edit_dish)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ci/progs/ruritania/menu/test_valid.py", line 64, in test_validate_page_edit_dish
    self.assertValid(reverse('edit_dish', args=[self.sausages.id]))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ci/progs/ruritania/core/common_test.py", line 31, in assertValid
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        result.returncode == 0,
        ^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
        )
        ^
    )
    ^
AssertionError: False is not true : The HTML is not valid
/menu/dish/1/edit
:127.1-127.109: error: The “aria-labelledby” attribute must not be specified on any “div” element unless the element has a “role” value other than “caption”, “code”, “deletion”, “emphasis”, “generic”, “insertion”, “paragraph”, “presentation”, “strong”, “subscript”, or “superscript”.
:142.21-142.79: error: Attribute “href” not allowed on element “button” at this point.
:131.17-131.62: error: The heading “h3” (with computed level 3) follows the heading “h1” (with computed level 1), skipping 1 heading level.
```
