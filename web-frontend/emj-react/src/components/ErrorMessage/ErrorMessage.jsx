import Button from "../UI/Button";

function ErrorMessage({
  title = "Erro ao carregar os dados",
  message = "Não foi possível carregar as informações no momento. Tente novamente em alguns instantes.",
  onRetry,
}) {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="text-center max-w-md flex flex-col justify-center items-center gap-4">
        <h1 className="text-xl font-semibold text-(--text-900) mb-3">
          {title}
        </h1>

        <p className="text-(--text-700) mb-6">{message}</p>

        {onRetry && (
          <Button onClick={onRetry} variant="export">
            Recarregar página
          </Button>
        )}
      </div>
    </div>
  );
}

export default ErrorMessage;
