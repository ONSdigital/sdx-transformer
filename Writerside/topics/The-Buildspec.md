<show-structure for="chapter" depth="2"/>

# The Buildspec

## Fields overview

Build specs are written either in yaml or json format with the following top level fields:

<table>
<tr>
    <td>Field</td>
    <td>Description</td>
    <td>Type</td>
    <td>Example</td>
</tr>
    
<tr>
    <td><code>title</code></td>
    <td>A descriptive title for the build spec</td>
    <td>string</td>
    <td>"Build Spec for Monthly Credit Grantors"</td>
</tr>

<tr>
    <td><code>survey_id</code></td>
    <td>The survey id for this particular survey</td>
    <td>string</td>
    <td>"127"</td>
</tr>

<tr>
    <td><code>period_format</code></td>
    <td>A string representing the format of the period as passed to SDX from upstream</td>
    <td>string</td>
    <td>"YYYYMM"</td>
</tr>

<tr>
    <td>
        <code>pck_period_format</code>
        <note>
            <p>
                Required for pck only
            </p>
        </note>
    </td>
    <td>The format of the period as it should be displayed on the pck</td>
    <td>string</td>
    <td>"YY"</td>
</tr>

<tr>
    <td><code>form_mapping</code></td>
    <td>An object mapping formtypes to idbr codes used in the pck</td>
    <td>object</td>
    <td>
        <code>{"0001": "STP01", "0011": "STE17"}</code>
    </td>
</tr>

<tr>
    <td>
        <code>item_list_path</code>
        <note>
            <p>
                Required for pre-pop only
            </p>
        </note>
    </td>
    <td>The XPath of the item subsets within a template</td>
    <td>object</td>
    <td>
        <code>{"0001": "STP01", "0011": "STE17"}</code>
    </td>
</tr>

<tr>
    <td><code>target</code></td>
    <td>The name of the target system. This will decide the formatting and shape of the output file</td>
    <td>string</td>
    <td>"OpenROAD"</td>
</tr>


<tr>
    <td><code>template</code></td>
    <td>A mapping of qcodes/identifiers to values/transforms. Explained in detail below</td>
    <td>object</td>
    <td>
        <code>{"001": "1", "002":"#045, "003":"$round"}</code>
    </td>
</tr>

<tr>
    <td><code>transforms</code></td>
    <td>The definition of the transforms used within the template. Explained in detail below	</td>
    <td>object</td>
    <td>
        <code>{"round":{"name": "ROUND", "args":{"nearest":"1000"}}}</code>
    </td>
</tr>
</table>

## Fields {id="fields-chapter"}

A more detailed description of each of the build spec fields

### title 

The title field

### survey_id 

Hello

### period_format 

Hello

### pck_period_format

Hello

### form_mapping

Hello

### item_list_path

Hello

### target

Hello

### template

The template section dictates both the 'shape' of the output data and how to determine its values.

<tabs>
<tab title="Template">

<code-block lang="json">
{
    "300": "Literal value",
    "301": "#301",
    "302": "$ROUND_THOUSAND",
    "400": "$CONTAINS",
    "500": "#500"
}
</code-block>

</tab>
<tab title="Input Data" id="input_data">

<code-block lang="json">
{
    "300": "56123",
    "301": "4567",
    "302": "1834",
    "400": "Yes",
    "500": "0-9%"
}
</code-block>


</tab>

<tab title="Output">

<code-block lang="json">
{
    "300": "Literal value",
    "301": "4567",
    "302": "2000",
    "400": "True",
    "500": "0-9%"
}
</code-block>

</tab>

</tabs>

<note>
    <p>
        We assume <code>$CONTAINS</code> is a transform that outputs "True" if it contains the string "Yes"
    </p>
</note>

It as a parametrised object that will be interpolated at runtime. The interpolation follows these rules:

#### # Symbols {collapsible="true" id=direct_lookup}
Values prefixed with a `#` will be looked up from the input data e.g. `#301` means lookup the value in the input data corresponding to key **"301"**. For the input data above this would resolve in the value **"4567"** at runtime (as 4567 corresponds to `301` in the Input Data .
  
Certain survey metadata can also be looked up. The allowed values are...

{style="medium"}
`#survey_id`
: Return the survey ID of the current survey

`#period_id`
: Return the period ID of the current survey

`#ru_ref`
: Return the ru_ref of the current survey

`#form_type`
: Return the form type for the current survey

`#period_start_date`
: Return the period start date for the current survey

`#period_end_date`
: Return the period end date for the current survey

#### $ Symbols {collapsible="true" id=transform_lookup}

<code-block lang="json">
{
    "template": {
        "42": "$ROUND",
    },
    "transforms": {
        "ROUND": {
            "name": "ROUND",
            "args": {
                "nearest": "1"
            }
        },
    }
}
</code-block>

Values prefixed with a `$` will be replaced with the result of performing the corresponding transform in the [Transforms](#transforms) section at runtime.

For example the value of `42` in the input data will be sent to the `$ROUND` transform which is defined in the `Transforms` section of the build spec

#### & Symbols {collapsible="true" id=computed_lookup}

<code-block lang="json">
{
    "template": {
        "42": "$ROUND",
        "43": "&42"
    },
    "transforms": {
        "ROUND": {
            "name": "ROUND",
            "args": {
                "nearest": "1"
            }
        },
    }
}
</code-block>

Values prefixed with a `&` will be looked up from the resulting output data.

For example, in the above snippet `&42` means, calculate the value for `42` as before using the `ROUND` transform, then assign the value to `43` which will result in codes `42` and `43` containing the same value.

#### No symbols (literals) {collapsible="true" id=literals}

<code-block lang="json">
{
    "template": {
        "42": "Hello world",
    },
}
</code-block>
Anything else will be considered as a literal and will remain unchanged at runtime.

In the example above, code `42` will be assigned to the value **"Hello world"**

### transforms {id=transforms}

The `transforms` section provides the definition for any transform identifier referenced in the [template](#template) section (as denoted with a `$` prefix). It is a set of key value mappings of identifier to definition. 

<code-block lang="json">
"transforms": {
    "ROUND_THOUSAND": {
      "name": "ROUND",
      "args": {
        "nearest": "1000"
      }
    },    
    "PERCENTAGE_RADIO": {
      "name": "LOOKUP",
      "args": {
        "0-9%": "10000",
        "10-24%": "1000",
        "25-49%": "100",
        "50-74%": "10",
        "75-100%": "1",
        "on_no_match": "0"
      }
    }
}
</code-block>

In the example above we define two transforms, `ROUND_THOUSAND` and `PERCENTAGE_RADIO`. The attributes each transform can have are defined below...

{style="full"}
name 
: Type: `string`
: A transform must specify a transformation function in the `name` attribute, in this case the transformation functions are `ROUND` and `LOOKUP` respectively. These functions need to be defined in `app/transform/execute.py` in the `_function_lookup` dictionary.


args
: Type: `object`
: Key value pairs representing the arguments to be passed to the function specified by the `name` attribute. For example the `ROUND` function can take an optional parameter `nearest` that specifies how the input should be rounded.


## Example Build Spec

Here we have an example build spec for the **qpses** survey, both a YAML and JSON example are provided.
<tabs>
<tab title="YAML">

```yaml
```
{src="qpses.yaml"}

</tab>
<tab title="JSON">

```json
```
{src="qpses.json"}


</tab>
</tabs>



