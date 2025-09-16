## Finding Somewhere to Start

Extract best-effort Java source using `jadx-gui basic_rev.apk`. The following is seen in `Source code/com/example.basic_rev/MainActivity`:

```java
public String makeFlag(String s) {
    String a = "" + s.charAt(5);
    String _b = s.charAt(2) + "";
    for (int s_ = 0; s_ < s.length(); s_++) {
        String b = _b.substring(_b.length() - s_) + _b.substring(s_);
        String _b2 = s_ >= 3 ? _b + s.charAt(s_ - 3) + "" : _b + s.charAt(s.length() - (3 - s_)) + "";
        if (s_ >= _b2.length()) {
            _b = _b2 + s.charAt(s_ - _b2.length()) + "";
        } else if (s.length() >= _b2.length() - s_) {
            _b = _b2 + s.charAt(s.length() - (_b2.length() - s_)) + "";
        } else {
            _b = _b2 + s.charAt(s.length() - ((_b2.length() - s_) - s.length())) + "";
        }
        a = a + b.charAt((((s.length() + _b.length()) * s_) + _b.length()) % b.length());
    }
    return a.substring(0, 2) + s.charAt(3) + a.charAt(3) + '0' + a.substring(5, 7);
}

protected void onCreate(...)  {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    this.b1 = (Button) findViewById(R.id.button);
    this.ed1 = (EditText) findViewById(R.id.editText);
    final String seed = getString(R.string.seed);
    this.b1.setOnClickListener(new View.OnClickListener() { // from class: com.example.basic_rev.MainActivity.1
        @Override // android.view.View.OnClickListener
        public void onClick(View v) {
            if (MainActivity.this.ed1.getText().toString().equals(MainActivity.this.makeFlag(seed))) {
                Toast.makeText(MainActivity.this.getApplicationContext(), "Well played! You can validate now with this password :)", 0).show();
            } else {
                Toast.makeText(MainActivity.this.getApplicationContext(), "Try again ;)", 0).show();
            }
        }
    });
}
```

Of note is the branch in `onClick`: `MainActivity.this.ed1.getText().toString().equals(MainActivity.this.makeFlag(seed))`.
Whatever text the user inputs into the text field gets compared to `MainActivity.this.makeFlag(seed)`. So we need two things:

1. A way to evaluate `makeFlag` given a seed string
2. The value of `seed`.

## Extracting `makeFlag`

> **NOTE:** you should be careful when ripping code and running it on your machine. In this case it is easy to see that the code we are 
> taking is only doing string operations, but other software may do much worse, especially malware. Exercise caution!

Since the code has been decompiled, we don't need to do much: just take the existing `makeFlag` method and turn it into a runnable program.
My version is `FlagMaker.java`, which we can run with `javac FlagMaker.java && java FlagMaker <seed>`.

## Finding the Seed

We can see that `seed` is defined to be `getString(R.string.seed)`. `R` is an Android idiom for "resources". So instead of continuing to follow
the Java source, we can navigate to `Resources/resources.arsc/res/values/strings.xml` and look for a resource named `seed`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- ... -->
    <string name="seed">1dndr@</string>
    <!-- ... -->
</resources>
```

## Finishing Up

We now have the value of `seed`, `1dndr@`, and a program to construct the flag from it, `FlagMaker.java`. Therefore we just invoke the maker with the seed:
`javac FlagMaker.java && java FlagMaker 1dndr@`:

```
Flag: @ndr01d
```
