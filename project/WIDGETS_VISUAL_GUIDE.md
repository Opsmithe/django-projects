# Django Widgets - Visual Guide

## Side-by-Side Comparison

### Example 1: Text Input

**Without Widget Customization:**
```python
class MemberForm(forms.ModelForm):
    class Meta:
        model = Names
        fields = ['firstname']
```

**HTML Output:**
```html
<input type="text" name="firstname" id="id_firstname">
```

**Browser Display:**
```
┌─────────────────────────────────┐
│                                 │  ← Plain, unstyled
└─────────────────────────────────┘
```

---

**With Widget Customization:**
```python
class MemberForm(forms.ModelForm):
    class Meta:
        model = Names
        fields = ['firstname']
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter first name',
            }),
        }
```

**HTML Output:**
```html
<input type="text" name="firstname" id="id_firstname" 
       class="form-input" placeholder="Enter first name">
```

**Browser Display:**
```
┌─────────────────────────────────┐
│ Enter first name                │  ← Styled with placeholder
└─────────────────────────────────┘
```

---

### Example 2: Email Input

**Default Widget:**
```python
email = models.EmailField()
```

**HTML:**
```html
<input type="email" name="email" id="id_email">
```

**Browser:**
```
┌─────────────────────────────────┐
│                                 │
└─────────────────────────────────┘
```

---

**Custom Widget:**
```python
widgets = {
    'email': forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'you@example.com',
        'autocomplete': 'email',
    }),
}
```

**HTML:**
```html
<input type="email" name="email" id="id_email" 
       class="form-input" placeholder="you@example.com" 
       autocomplete="email">
```

**Browser:**
```
┌─────────────────────────────────┐
│ you@example.com                 │  ← Styled with hint
└─────────────────────────────────┘
```

---

### Example 3: Select Dropdown

**Default Widget:**
```python
status = models.CharField(choices=Status.choices)
```

**HTML:**
```html
<select name="status" id="id_status">
    <option value="NPL">Not Played</option>
    <option value="PL">Played</option>
</select>
```

**Browser:**
```
┌─────────────────────────────────┐
│ Not Played              ▼       │  ← Plain dropdown
└─────────────────────────────────┘
```

---

**Custom Widget:**
```python
widgets = {
    'status': forms.Select(attrs={
        'class': 'form-select',
    }),
}
```

**HTML:**
```html
<select name="status" id="id_status" class="form-select">
    <option value="NPL">Not Played</option>
    <option value="PL">Played</option>
</select>
```

**Browser:**
```
┌─────────────────────────────────┐
│ Not Played              ▼       │  ← Styled dropdown
└─────────────────────────────────┘
```

---

### Example 4: Textarea

**Default Widget:**
```python
bio = models.TextField()
```

**HTML:**
```html
<textarea name="bio" id="id_bio"></textarea>
```

**Browser:**
```
┌─────────────────────────────────┐
│                                 │
│                                 │
│                                 │
└─────────────────────────────────┘
```

---

**Custom Widget:**
```python
widgets = {
    'bio': forms.Textarea(attrs={
        'class': 'form-textarea',
        'rows': 5,
        'placeholder': 'Tell us about yourself...',
    }),
}
```

**HTML:**
```html
<textarea name="bio" id="id_bio" class="form-textarea" 
          rows="5" placeholder="Tell us about yourself..."></textarea>
```

**Browser:**
```
┌─────────────────────────────────┐
│ Tell us about yourself...       │
│                                 │
│                                 │
│                                 │
│                                 │
└─────────────────────────────────┘
```

---

## Widget Types Visual Reference

### Text-Based Widgets

```
TextInput
┌─────────────────────────────────┐
│ Single line text                │
└─────────────────────────────────┘

EmailInput
┌─────────────────────────────────┐
│ email@example.com               │
└─────────────────────────────────┘

PasswordInput
┌─────────────────────────────────┐
│ ••••••••                        │
└─────────────────────────────────┘

NumberInput
┌─────────────────────────────────┐
│ 42                          ▲▼  │
└─────────────────────────────────┘

URLInput
┌─────────────────────────────────┐
│ https://example.com             │
└─────────────────────────────────┘

Textarea
┌─────────────────────────────────┐
│ Multiple                        │
│ lines                           │
│ of text                         │
└─────────────────────────────────┘
```

### Selection Widgets

```
Select (Dropdown)
┌─────────────────────────────────┐
│ Option 1                    ▼   │
└─────────────────────────────────┘
  ├─ Option 1
  ├─ Option 2
  └─ Option 3

RadioSelect
○ Option 1
○ Option 2
● Option 3  ← Selected

CheckboxInput
☑ I agree to terms

CheckboxSelectMultiple
☑ Option 1
☐ Option 2
☑ Option 3
```

### Date/Time Widgets

```
DateInput
┌─────────────────────────────────┐
│ 02/26/2026              📅      │
└─────────────────────────────────┘

TimeInput
┌─────────────────────────────────┐
│ 14:30                   🕐      │
└─────────────────────────────────┘

DateTimeInput
┌─────────────────────────────────┐
│ 02/26/2026 14:30        📅🕐    │
└─────────────────────────────────┘
```

### Special Widgets

```
HiddenInput
(Not visible to user)

FileInput
┌─────────────────────────────────┐
│ Choose File    No file chosen   │
└─────────────────────────────────┘

ClearableFileInput
┌─────────────────────────────────┐
│ Currently: image.jpg            │
│ ☐ Clear                         │
│ Change: [Choose File]           │
└─────────────────────────────────┘
```

---

## Attribute Effects Visual Guide

### Placeholder

**Without:**
```
┌─────────────────────────────────┐
│ |                               │  ← Cursor, no hint
└─────────────────────────────────┘
```

**With:**
```
┌─────────────────────────────────┐
│ Enter your name...              │  ← Gray hint text
└─────────────────────────────────┘
```

### Required

**Without:**
```
┌─────────────────────────────────┐
│                                 │
└─────────────────────────────────┘
```

**With:**
```
Name *                              ← Asterisk indicator
┌─────────────────────────────────┐
│                                 │
└─────────────────────────────────┘
```

### Disabled

**Normal:**
```
┌─────────────────────────────────┐
│ Editable text                   │  ← White background
└─────────────────────────────────┘
```

**Disabled:**
```
┌─────────────────────────────────┐
│ Cannot edit                     │  ← Gray background
└─────────────────────────────────┘
```

### Readonly

**Normal:**
```
┌─────────────────────────────────┐
│ Can edit                        │  ← Can type
└─────────────────────────────────┘
```

**Readonly:**
```
┌─────────────────────────────────┐
│ Cannot edit but can select      │  ← Can select text
└─────────────────────────────────┘
```

### Maxlength

**Without:**
```
┌─────────────────────────────────┐
│ User can type unlimited text... │
└─────────────────────────────────┘
```

**With maxlength="10":**
```
┌─────────────────────────────────┐
│ Only 10 ch                      │  ← Stops at 10
└─────────────────────────────────┘
```

---

## CSS Class Effects

### Without CSS Class

```python
widgets = {
    'firstname': forms.TextInput(),
}
```

**Browser:**
```
┌─────────────────────────────────┐
│                                 │  ← Browser default styling
└─────────────────────────────────┘
```

### With CSS Class

```python
widgets = {
    'firstname': forms.TextInput(attrs={
        'class': 'form-input',
    }),
}
```

**CSS:**
```css
.form-input {
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 5px;
}
```

**Browser:**
```
┌─────────────────────────────────┐
│                                 │  ← Custom styled
└─────────────────────────────────┘
  ↑ Padding, border, rounded corners
```

---

## Mobile Keyboard Behavior

### TextInput (type="text")
```
┌─────────────────────────────────┐
│ Q W E R T Y U I O P             │
│  A S D F G H J K L              │
│   Z X C V B N M                 │
│     [space]                     │
└─────────────────────────────────┘
Standard keyboard
```

### EmailInput (type="email")
```
┌─────────────────────────────────┐
│ Q W E R T Y U I O P             │
│  A S D F G H J K L              │
│   Z X C V B N M @ .             │
│     [space]                     │
└─────────────────────────────────┘
@ and . easily accessible
```

### NumberInput (type="number")
```
┌─────────────────────────────────┐
│     1   2   3                   │
│     4   5   6                   │
│     7   8   9                   │
│     .   0   ⌫                   │
└─────────────────────────────────┘
Numeric keypad
```

### URLInput (type="url")
```
┌─────────────────────────────────┐
│ Q W E R T Y U I O P             │
│  A S D F G H J K L              │
│   Z X C V B N M / .             │
│     [space]                     │
└─────────────────────────────────┘
/ and . easily accessible
```

---

## Form Validation Visual States

### Valid Input
```
First Name *
┌─────────────────────────────────┐
│ John                            │  ← Green border
└─────────────────────────────────┘
✓ Looks good!
```

### Invalid Input
```
First Name *
┌─────────────────────────────────┐
│                                 │  ← Red border
└─────────────────────────────────┘
⚠ This field is required.
```

### Focus State
```
First Name *
┌═════════════════════════════════┐
│ |                               │  ← Blue glow
└═════════════════════════════════┘
```

---

## Complete Form Example

**Code:**
```python
class MemberForm(forms.ModelForm):
    class Meta:
        model = Names
        fields = ['firstname', 'email', 'status']
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter first name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'you@example.com',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
```

**Visual Result:**
```
┌─────────────────────────────────────────────┐
│  Add New Member                             │
├─────────────────────────────────────────────┤
│                                             │
│  First Name *                               │
│  ┌───────────────────────────────────────┐  │
│  │ Enter first name                      │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  Email *                                    │
│  ┌───────────────────────────────────────┐  │
│  │ you@example.com                       │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  Status                                     │
│  ┌───────────────────────────────────────┐  │
│  │ Not Played                        ▼   │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ Create Member│  │    Cancel    │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────┘
```

---

## Summary

**Widgets transform this:**
```html
<input type="text" name="firstname">
```

**Into this:**
```html
<input type="text" name="firstname" id="id_firstname"
       class="form-input" placeholder="Enter first name"
       maxlength="50" required>
```

**Which looks like this:**
```
First Name *
┌─────────────────────────────────┐
│ Enter first name                │  ← Styled, with placeholder
└─────────────────────────────────┘
```

**Instead of this:**
```
┌─────────────────────────────────┐
│                                 │  ← Plain, no styling
└─────────────────────────────────┘
```

Widgets are the **styling and behavior layer** of your forms!
