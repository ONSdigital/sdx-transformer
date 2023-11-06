<show-structure for="chapter" depth="2"/>

# The Buildspec

## Format overview

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

### title {collapsible="true"}

The title field

### survey_id {collapsible="true"}

Hello

### period_format {collapsible="true"}

Hello

### pck_period_format {collapsible="true"}

Hello

### form_mapping {collapsible="true"}

Hello

### item_list_path {collapsible="true"}

Hello

### target {collapsible="true"}

Hello

### template {collapsible="true"}

<code-block lang="json">
{
    "300": "56123",
    "301": "4567",
    "302": "1834",
    "400": "Yes",
    "500": "0-9%"
}
</code-block>
The template section dictates both the 'shape' of the output data and how to determine its values. It as a parametrised object that will be interpolated at runtime. The interpolation follows these rules:

#### # Symbols {id=direct_lookup}
Values prefixed with a `#` will be looked up from the input data e.g. `#301` means lookup the value in the input data corresponding to key **"301"**. For the input data above this would resolve in the value **"4567"** at runtime.
  
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

#### $ Symbols {id=transform_lookup}

Values prefixed with a `$` will be replaced with the result of performing the corresponding transform in the [Transforms](#transforms) section at runtime. E.g. "$ROUND".

- Values prefixed with a "&" will be looked up from the resulting output data e.g. "&301" means lookup the calculated value for 301.
- Anything else will be considered as a literal and will remain unchanged at runtime.

### transforms {collapsible="true" id=transforms}

Hello

## Example Build Spec

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



