import json
import sys
from typing import Optional

import click

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL
from .exceptions import PepkioError


@click.group()
@click.option(
    "--base-url",
    envvar="PEPKIO_API_BASE_URL",
    default=DEFAULT_API_BASE_URL,
    help="Base URL for Pepkio API (default: https://tools.pepkio.com)",
)
@click.option(
    "--api-key",
    envvar="PEPKIO_API_KEY",
    default=None,
    help="Pepkio API bearer key",
)
@click.option(
    "--no-verify",
    is_flag=True,
    default=False,
    help="Disable SSL certificate verification (useful for local development)",
)
@click.pass_context
def main(ctx: click.Context, base_url: str, api_key: Optional[str], no_verify: bool):
    """CLI for Pepkio codon-host-fit-checker tool."""
    ctx.ensure_object(dict)
    verify_ssl = not no_verify
    if "localtest.me" in base_url and not no_verify:
        verify_ssl = False
    ctx.obj["client"] = PepkioClient(api_key=api_key, base_url=base_url, verify_ssl=verify_ssl)


@main.command()
@click.pass_context
def manifest(ctx: click.Context):
    """Fetch and display the tool manifest."""
    client: PepkioClient = ctx.obj["client"]
    try:
        manifest_data = client.get_manifest()
        click.echo(json.dumps(manifest_data, indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--input-json",
    type=str,
    help="Tool input JSON string",
)
@click.option(
    "--input-file",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to JSON file containing tool input",
)
@click.option(
    "--example",
    type=str,
    help="Name of manifest example to run (e.g. gfp_matrix)",
)
@click.option(
    "--idempotency-key",
    type=str,
    help="Optional idempotency key for the run",
)
@click.option(
    "--label",
    type=str,
    help="Optional label for the run",
)
@click.pass_context
def run(
    ctx: click.Context,
    input_json: Optional[str],
    input_file: Optional[str],
    example: Optional[str],
    idempotency_key: Optional[str],
    label: Optional[str],
):
    """Execute the codon-host-fit-checker tool."""
    client: PepkioClient = ctx.obj["client"]
    input_data = None

    if example:
        try:
            m = client.get_manifest()
            examples = m.get("examples", [])
            matched = next((ex for ex in examples if ex.get("name") == example), None)
            if not matched:
                names = ", ".join([ex.get("name", "") for ex in examples])
                click.echo(f"Error: Example '{example}' not found. Available: {names}", err=True)
                sys.exit(1)
            input_data = matched.get("input")
        except PepkioError as e:
            click.echo(f"Error fetching manifest for example: {e}", err=True)
            sys.exit(1)
    elif input_json:
        try:
            input_data = json.loads(input_json)
        except json.JSONDecodeError as e:
            click.echo(f"Error parsing --input-json: {e}", err=True)
            sys.exit(1)
    elif input_file:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                input_data = json.load(f)
        except Exception as e:
            click.echo(f"Error reading --input-file: {e}", err=True)
            sys.exit(1)
    else:
        click.echo("Error: Must provide one of --input-json, --input-file, or --example", err=True)
        sys.exit(1)

    try:
        result = client.run(
            input_data=input_data,
            idempotency_key=idempotency_key,
            label=label,
        )
        click.echo(json.dumps(result.model_dump(), indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command(name="get-run")
@click.argument("run_id", type=str)
@click.pass_context
def get_run(ctx: click.Context, run_id: str):
    """Retrieve status and results of a run by ID."""
    client: PepkioClient = ctx.obj["client"]
    try:
        result = client.get_run(run_id)
        click.echo(json.dumps(result.model_dump(), indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
